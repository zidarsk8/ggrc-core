# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

import logging
from collections import namedtuple

from sqlalchemy import or_, and_

from ggrc import models
from ggrc.models.relationship import Relationship
from ggrc.services.common import Resource
from ggrc import db
from ggrc.automapper.rules import rules
from ggrc.utils import benchmark, with_nop
from ggrc.rbac.permissions import is_allowed_update


class Stub(namedtuple("Stub", ["type", "id"])):

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
    self.cache = dict()
    self.auto_mappings = set()
    if use_benchmark:
      self.benchmark = benchmark
    else:
      self.benchmark = with_nop

  def related(self, obj):
    if obj in self.cache:
      return self.cache[obj]
    relationships = Relationship.query.filter(or_(
        and_(Relationship.source_type == obj.type,
             Relationship.source_id == obj.id),
        and_(Relationship.destination_type == obj.type,
             Relationship.destination_id == obj.id),
    )).all()
    res = set((Stub.from_destination(r)
               if r.source_type == obj.type and r.source_id == obj.id
               else Stub.from_source(r))
              for r in relationships)
    self.cache[obj] = res
    return res

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
    with self.benchmark("Automapping flush"):
      db.session.add_all(Relationship(
          source_type=src.type,
          source_id=src.id,
          destination_type=dst.type,
          destination_id=dst.id,
          automapping_id=self.relationship.id
      ) for src, dst in self.auto_mappings)
      db.session.flush()

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
