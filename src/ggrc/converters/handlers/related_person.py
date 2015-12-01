# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc.converters.handlers import handlers

from sqlalchemy import and_

from ggrc import db
from ggrc.converters import errors
from ggrc import models


class RelatedPersonColumnHandler(handlers.UserColumnHandler):

  _assigne_type = None

  def parse_item(self):
    users = self.get_users_list()
    if self.mandatory and not users:
      self.add_error(errors.MISSING_VALUE_ERROR, column_name=self.display_name)
    return users

  def set_obj_attr(self):
    self.value = self.parse_item()

  def _create_relationship_attr(self, relation):
    rel_attr = models.RelationshipAttr(
        attr_name="AssigneeType",
        attr_value=self._assigne_type,
        relationship_id=relation.id
    )
    db.session.add(rel_attr)
    db.session.flush()

  def _remove_relationship_attr(self):
    """ Remove all instances of a relationship attr and value

    This function is used for example to clean up all Assignees from requests.
    """
    relations = models.Relationship.get_related_query(
        self.row_converter.obj, models.Person()
    ).join(models.RelationshipAttr).filter(
        models.RelationshipAttr.attr_name == "AssigneeType"
    ).all()
    for relation in relations:
      rel_attr = relation.relationship_attrs["AssigneeType"]
      values = rel_attr.attr_value.split(",")
      filtered_values = [v for v in values if v != self._assigne_type]
      rel_attr.attr_value = ",".join(filtered_values)
    db.session.flush()

  def _create_relationship(self, person):
    relation = models.Relationship(
        source_type=person.type,
        source_id=person.id,
        destination_type=self.row_converter.obj.type,
        destination_id=self.row_converter.obj.id
    )
    db.session.add(relation)
    db.session.flush()
    self._create_relationship_attr(relation)

  def _update_relationship_attr(self, rel_attr, person):
    values = set(rel_attr.attr_value.split(","))
    values.add(self._assigne_type)
    rel_attr.attr_value = ",".join(values)
    db.session.flush()

  def insert_object(self):
    self._remove_relationship_attr()
    for person in self.value:
      relation = models.Relationship.find_related(
          self.row_converter.obj, person)
      if relation is None:
        self._create_relationship(person)
      elif relation.relationship_attrs is None or \
              "AssigneeType" not in relation.relationship_attrs:
        self._create_relationship_attr(relation)
      else:
        self._update_relationship_attr(
            relation.relationship_attrs["AssigneeType"], person)

  def get_value(self):
    """ Get a list of people with specific role on a Request """
    RA = models.RelationshipAttr
    relations = models.Relationship.get_related_query(
        self.row_converter.obj, models.Person()
    ).join(RA).filter(and_(
        RA.attr_name == "AssigneeType",
        RA.attr_value.contains(self._assigne_type),
    )).all()
    people_ids = [r.source_id for r in relations if r.source_type == "Person"]
    people_ids.extend(
        [r.destination_id for r in relations if r.destination_type == "Person"]
    )
    emails = []
    if people_ids:
      people = models.Person.query.filter(
          models.Person.id.in_(people_ids)).all()
      emails = [p.email for p in people]
    return "\n".join(emails)


class RelatedAssigneesColumnHandler(RelatedPersonColumnHandler):

  def __init__(self, row_converter, key, **options):
    self._assigne_type = "Assignee"
    super(self.__class__, self).__init__(row_converter, key, **options)


class RelatedRequestersColumnHandler(RelatedPersonColumnHandler):

  def __init__(self, row_converter, key, **options):
    self._assigne_type = "Requester"
    super(self.__class__, self).__init__(row_converter, key, **options)


class RelatedVerifiersColumnHandler(RelatedPersonColumnHandler):

  def __init__(self, row_converter, key, **options):
    self._assigne_type = "Verifier"
    super(self.__class__, self).__init__(row_converter, key, **options)
