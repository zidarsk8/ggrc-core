# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

import logging

from ggrc.models.relationship import Relationship
from ggrc.services.common import Resource
from ggrc import db
from ggrc.automapper.rules import rules
from ggrc.utils import benchmark


class AutomapperGenerator(object):
  def __init__(self, relationship):
    self.relationship = relationship
    self.processed = set()
    self.queue = set()

  def related(self, obj):
    with benchmark("Automapping related"):
      return (set(r.source for r in obj.related_sources) |
              set(r.destination for r in obj.related_destinations))

  def relate(self, src, dst):
    if src < dst:
      return (src, dst)
    else:
      return (dst, src)

  def generate_automappings(self):
    with benchmark("Automapping generate_automappings"):
        self.queue.add(self.relate(self.relationship.source,
                       self.relationship.destination))
        while len(self.queue) > 0:
          src, dst = entry = self.queue.pop()
          # TODO check that user can see both objects
          self._ensure_relationship(src, dst)
          self.processed.add(entry)
          self._step(src, dst)
          self._step(dst, src)

  def _step(self, src, dst):
    with benchmark("Automapping _step"):
      explicit, implicit = rules[src.type, dst.type]
      self._step_explicit(src, dst, explicit)
      self._step_implicit(src, dst, implicit)

  def _step_explicit(self, src, dst, explicit):
    with benchmark("Automapping _step_explicit"):
      if len(explicit) != 0:
        src_related = (o for o in self.related(src)
                       if o.type in explicit and o != dst)
        for r in src_related:
          entry = self.relate(r, dst)
          if entry not in self.processed:
            self.queue.add(entry)

  def _step_implicit(self, src, dst, implicit):
    with benchmark("Automapping _step_implicit"):
      for attr in implicit:
        if hasattr(src, attr.name):
          attr = getattr(src, attr.name)
          entry = self.relate(attr, dst)
          if entry not in self.processed:
            self.queue.add(entry)
        else:
          logging.warning(
              'Automapping by attr: object %s has no attribute %s' %
              (str(src), str(attr.name))
          )

  def _ensure_relationship(self, src, dst):
    with benchmark("Automapping _ensure_relationship"):
      if Relationship.find_related(src, dst) is None:
        db.session.add(Relationship(
            source=src,
            destination=dst,
            automapping_id=self.relationship.id
        ))


def register_automapping_listeners():
  @Resource.model_posted.connect_via(Relationship)
  def handle_relationship_post(sender, obj=None, src=None, service=None):
    if obj is None:
      logging.warning("Automapping listener: no obj, no mappings created")
      return
    AutomapperGenerator(obj).generate_automappings()
