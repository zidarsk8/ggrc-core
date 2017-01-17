# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Contains the Assignable mixin.

This allows adding various assignee types to the object, like Verifier,
Requester, etc.
"""

from sqlalchemy import and_
from sqlalchemy import or_
from ggrc.models import person
from ggrc import db
from ggrc.models import relationship


class Assignable(object):
  """Mixin for models with assignees"""

  ASSIGNEE_TYPES = set(["Assignee"])

  @property
  def assignees(self):
    """Property that returns assignees

    Returns:
        A set of assignees.
    """

    assignees = [(r.source, tuple(r.attrs["AssigneeType"].split(",")))
                 for r in self.related_sources
                 if "AssigneeType" in r.attrs]
    assignees += [(r.destination, tuple(r.attrs["AssigneeType"].split(",")))
                  for r in self.related_destinations
                  if "AssigneeType" in r.attrs]
    return assignees

  def get_assignees(self, filter_=None):
    """Get assignees by type.

    This is helper for fetching only specific assignee types.

    Args:
      filter_: String containing assignee type or a list with desired assignee
        types. If None, all assignees are returned (see self.assignees).

    Returs:
      Filtered list of assignees.
    """
    if filter_ is None:
      return self.assignees
    elif isinstance(filter_, basestring):
      filter_ = [filter_]

    filter_set = set(filter_)

    return [(person_, roles) for person_, roles in self.assignees
            if filter_set.intersection(roles)]

  @staticmethod
  def _validate_relationship_attr(class_, source, dest, existing, name, value):
    """Validator that allows Assignable relationship attributes

    Allow relationship attribute of name "AssigneeType" with value that is a
    comma separated list of valid roles (as defined in target class).

    Args:
        class_ (class): target class of this mixin. Think of this like a class
                     method.
        source (model instance): relevant relationship source
        dest (model instance): relevant relationship destinations
        existing (dict): current attributes on the relationship
        name (string): attribute name
        value (any): attribute value. Should be string for the right attribute

    Returns:
        New attribute value (merge with existing roles) or None if the
        attribute is not valid.
    """
    if set([source.type, dest.type]) != set([class_.__name__, "Person"]):
      return None
    if name != "AssigneeType":
      return None
    new_roles = value.split(",")
    if not all(role in class_.ASSIGNEE_TYPES for role in new_roles):
      return None
    roles = set(existing.get(name, "").split(",")) | set(new_roles)
    return ",".join(role for role in roles if role)

  @classmethod
  def _get_relate_filter(cls, predicate, related_type):
    """Used for filtering by related_assignee.

    Returns:
        Boolean stating whether such an assignee exists.
    """
    # pylint: disable=invalid-name
    # The upper case variables are allowed here to shorthand the class names.
    Rel = relationship.Relationship
    RelAttr = relationship.RelationshipAttr
    Person = person.Person
    return db.session.query(Rel).join(RelAttr).join(
        Person,
        or_(and_(
            Rel.source_id == Person.id,
            Rel.source_type == Person.__name__
        ), and_(
            Rel.destination_id == Person.id,
            Rel.destination_type == Person.__name__
        ))
    ).filter(and_(
        RelAttr.attr_value.contains(related_type),
        RelAttr.attr_name == "AssigneeType",
        or_(and_(
            Rel.source_type == Person.__name__,
            Rel.destination_type == cls.__name__,
            Rel.destination_id == cls.id
        ), and_(
            Rel.destination_type == Person.__name__,
            Rel.source_type == cls.__name__,
            Rel.source_id == cls.id
        )),
        or_(predicate(Person.name), predicate(Person.email))
    )).exists()
