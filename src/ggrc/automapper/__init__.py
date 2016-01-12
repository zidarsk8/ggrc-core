# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

from datetime import datetime
from ggrc import db
from ggrc import models
from ggrc.automapper.rules import rules
from ggrc.login import get_current_user
from ggrc.models.relationship import Relationship
from ggrc.models.request import Request
from ggrc.rbac.permissions import is_allowed_update
from ggrc.services.common import Resource
from ggrc.utils import benchmark, with_nop
from sqlalchemy.sql.expression import tuple_
import collections
import logging


class Stub(collections.namedtuple("Stub", ["type", "id"])):

  @classmethod
  def from_source(cls, relationship):
    return Stub(relationship.source_type, relationship.source_id)

  @classmethod
  def from_destination(cls, relationship):
    return Stub(relationship.destination_type, relationship.destination_id)


class AutomapperGenerator(object):
  def __init__(self, relationship, use_benchmark=True):
    self.relationship = relationship
    self.processed = set()
    self.queue = set()
    self.cache = collections.defaultdict(set)
    self.auto_mappings = set()
    if use_benchmark:
      self.benchmark = benchmark
    else:
      self.benchmark = with_nop

  def related(self, obj):
    if obj in self.cache:
      return self.cache[obj]
    # Pre-fetch neighbourhood for enqueued object since we're gonna need that
    # results in a few steps. This drastically reduces number of queries.
    stubs = {s for rel in self.queue for s in rel}
    stubs.add(obj)
    # Union is here to convince mysql to use two separate indices and
    # merge te results. Just using `or` results in a full-table scan
    relationships = Relationship.query.filter(
        tuple_(Relationship.source_type, Relationship.source_id).in_(
            [(s.type, s.id) for s in stubs]
        )
    ).union_all(
        Relationship.query.filter(
            tuple_(Relationship.destination_type,
                   Relationship.destination_id).in_(
                [(s.type, s.id) for s in stubs]
            )
        )
    ).all()
    for r in relationships:
      src = Stub.from_source(r)
      dst = Stub.from_destination(r)
      # only store a neighbour if we queried for it since this way we know
      # we'll be storing complete neighbourhood by the end of the loop
      if src in stubs:
        self.cache[src].add(dst)
      if dst in stubs:
        self.cache[dst].add(src)

    return self.cache[obj]

  def relate(self, src, dst):
    if src < dst:
      return (src, dst)
    else:
      return (dst, src)

  def generate_automappings(self):
    with self.benchmark("Automapping generate_automappings"):
      self.queue.add(self.relate(Stub.from_source(self.relationship),
                     Stub.from_destination(self.relationship)))
      count = 0
      while len(self.queue) > 0:
        if len(self.auto_mappings) > rules.count_limit:
          break
        count += 1
        src, dst = entry = self.queue.pop()

        if not (self._can_map_to(src) and self._can_map_to(dst)):
          continue

        self._ensure_relationship(src, dst)
        self.processed.add(entry)
        self._step(src, dst)
        self._step(dst, src)

      if len(self.auto_mappings) <= rules.count_limit:
        self._flush()
      else:
        self.relationship._json_extras = {
            'automapping_limit_exceeded': True
        }

  def _can_map_to(self, obj):
    return is_allowed_update(obj.type, obj.id, self.relationship.context)

  def _flush(self):
    if len(self.auto_mappings) == 0:
      return
    with self.benchmark("Automapping flush"):
      current_user = get_current_user()
      now = datetime.now()
      # We are doing an INSERT IGNORE INTO here to mitigate a race condition
      # that happens when multiple simultaneous requests create the same
      # automapping. If a relationship object fails our unique constraint
      # it means that the mapping was already created by another request
      # and we can safely ignore it.
      inserter = Relationship.__table__.insert().prefix_with("IGNORE")
      original = self.relate(Stub.from_source(self.relationship),
                             Stub.from_destination(self.relationship))
      db.session.execute(inserter.values([{
          "id": None,
          "modified_by_id": current_user.id,
          "created_at": now,
          "updated_at": now,
          "source_id": src.id,
          "source_type": src.type,
          "destination_id": dst.id,
          "destination_type": dst.type,
          "context_id": None,
          "status": None,
          "automapping_id": self.relationship.id}
          for src, dst in self.auto_mappings
          if (src, dst) != original]))  # (src, dst) is sorted

  def _step(self, src, dst):
      explicit, implicit = rules[src.type, dst.type]
      self._step_explicit(src, dst, explicit)
      self._step_implicit(src, dst, implicit)

  def _step_explicit(self, src, dst, explicit):
    if len(explicit) != 0:
      src_related = (o for o in self.related(src)
                     if o.type in explicit and o != dst)
      for r in src_related:
        entry = self.relate(r, dst)
        if entry not in self.processed:
          self.queue.add(entry)

  def _step_implicit(self, src, dst, implicit):
    if not hasattr(models, src.type):
      logging.warning('Automapping by attr: cannot find model %s' % src.type)
      return
    model = getattr(models, src.type)
    instance = model.query.filter(model.id == src.id).first()
    if instance is None:
      logging.warning("Automapping by attr: cannot load model %s: %s" %
                      (src.type, str(src.id)))
      return
    for attr in implicit:
      if hasattr(instance, attr.name):
        value = getattr(instance, attr.name)
        if value is not None:
          entry = self.relate(Stub(value.type, value.id), dst)
          if entry not in self.processed:
            self.queue.add(entry)
        else:
          logging.warning('Automapping by attr: %s is None' % attr.name)
      else:
        logging.warning(
            'Automapping by attr: object %s has no attribute %s' %
            (str(src), str(attr.name))
        )

  def _ensure_relationship(self, src, dst):
    if dst in self.cache.get(src, []):
      return
    if src in self.cache.get(dst, []):
      return

    if Relationship.find_related(src, dst) is None:
      self.auto_mappings.add((src, dst))

    if src in self.cache:
      self.cache[src].add(dst)
    if dst in self.cache:
      self.cache[dst].add(src)


def register_automapping_listeners():
  @Resource.model_posted.connect_via(Relationship)
  def handle_relationship_post(sender, obj=None, src=None, service=None):
    if obj is None:
      logging.warning("Automapping listener: no obj, no mappings created")
      return
    AutomapperGenerator(obj).generate_automappings()

  @Resource.model_posted_after_commit.connect_via(Request)
  @Resource.model_put_after_commit.connect_via(Request)
  def handle_request(sender, obj=None, src=None, service=None):
    if obj is None:
      logging.warning("Automapping request listener: "
                      "no obj, no mappings created")
      return
    if obj.audit is None:
      logging.warning("Automapping request listener: "
                      "no audit, no mappings created")
      return
    rel = Relationship(source_type=obj.type,
                       source_id=obj.id,
                       destination_type=obj.audit.type,
                       destination_id=obj.audit.id)
    handle_relationship_post(sender, obj=rel)
