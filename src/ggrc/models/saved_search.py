# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
  Module contains definition for SavedSearch model.

  SavedSearch model is used for storing query API
  requests allowing users to save their searches
  and share them with other users (sharing is
  implemented on FE side).
"""

import json

from sqlalchemy.orm import validates
from sqlalchemy.schema import UniqueConstraint

from ggrc import db
from ggrc.models.exceptions import ValidationError
from ggrc.models.mixins.base import CreationTimeTracked, Dictable, Identifiable
from ggrc.utils.contributed_objects import CONTRIBUTED_OBJECTS

SUPPORTED_OBJECT_TYPES = tuple(
    model.__name__ for model in CONTRIBUTED_OBJECTS,
)


class SavedSearch(CreationTimeTracked, Dictable, Identifiable, db.Model):
  """
    Represents table which stores queary API filters for
    given user.
  """

  __tablename__ = "saved_searches"
  __table_args__ = (
      UniqueConstraint(
          "person_id",
          "name",
          name="unique_pair_saved_search_name_person_id",
      ),
  )

  VALID_SAVED_SEARCH_TYPES = ["AdvancedSearch", "GlobalSearch"]

  name = db.Column(db.String, nullable=False)
  object_type = db.Column(db.String, nullable=False)
  person_id = db.Column(db.Integer, db.ForeignKey("people.id"))
  filters = db.Column(db.Text, nullable=True)
  type = db.Column(db.String, nullable=False)

  # pylint: disable-msg=too-many-arguments
  def __init__(self, name, object_type, user, type, filters=""):
    self.validate_name_uniqueness_for_user(user, name)

    super(SavedSearch, self).__init__(
        name=name,
        object_type=object_type,
        person_id=user.id,
        type=type,
        filters=filters,
    )

  def validate_name_uniqueness_for_user(self, user, name):
    """
      Check that for given user there are no saved searches
      with given name.
    """
    if user.saved_searches.filter(SavedSearch.name == name).count() > 0:
      raise ValidationError(
          u"Saved search with name '{}' already exists".format(name)
      )

  @validates("name")
  def validate_name(self, _, name):
    """
      Validate that name is not blank.
    """
    if not name:
      raise ValidationError("Saved search name can't be blank")

    return name

  @validates("object_type")
  def validate_object_type(self, _, object_type):
    """
      Validate that supplied object type supports search api filters saving.
    """
    if object_type not in SUPPORTED_OBJECT_TYPES:
      raise ValidationError(
          u"Object of type '{}' does not support search saving".format(
              object_type,
          ),
      )

    return object_type

  @validates("filters")
  def validate_filters(self, _, filters):
    """
      Validate correctness of supplied search filters.
    """
    if filters:
      return json.dumps(filters)
    return None

  @validates('type')
  def validate_type(self, _, type):
    """"""
    if not type:
      raise ValidationError("Saved search type can't be blank")

    if type not in self.VALID_SAVED_SEARCH_TYPES:
      raise ValidationError("Invalid saved search type")

    return type
