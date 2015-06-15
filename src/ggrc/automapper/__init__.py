# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

import logging

from ggrc.models.relationship import Relationship
from ggrc.services.common import Resource
from ggrc import db
from .rules import rules


def register_automapping_listeners():
  @Resource.model_posted.connect_via(Relationship)
  def handle_relationship_post(sender, obj=None, src=None, service=None):
    if obj is None:
      logging.warning("Automapping listener: no obj, no mappings created")
      return
    generate_automappings_for_relationship(obj)


def generate_automappings_for_relationship(relationship):
    processed = set()
    queue = set()

    def related(obj):
      return (set(r.source for r in obj.related_sources) |
              set(r.destination for r in obj.related_destinations))

    def relate(src, dst):
      if src < dst:
        return (src, dst)
      else:
        return (dst, src)

    queue.add(relate(relationship.source, relationship.destination))
    db_session = db.session

    def go(src, dst):
      explicit, implicit = rules[src.type, dst.type]
      if len(explicit) != 0:
        src_related = filter(lambda o: o.type in explicit, related(src))
        for r in src_related:
          if r == dst:
            continue
          entry = relate(r, dst)
          if entry not in processed:
            queue.add(entry)
      for attr in implicit:
        if hasattr(src, attr.name):
          attr = getattr(src, attr.name)
          entry = relate(attr, dst)
          if entry not in processed:
            queue.add(entry)
        else:
          logging.warning(
              'Automapping by attr: object %s has no attribute %s' %
              (str(src), str(attr.name))
          )

    while len(queue) > 0:
      src, dst = entry = queue.pop()
      if Relationship.find_related(src, dst) is None:
        db_session.add(Relationship(
            source=src,
            destination=dst,
            automapping_id=relationship.id
        ))
      processed.add(entry)
      go(src, dst)
      go(dst, src)
