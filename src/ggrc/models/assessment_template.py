# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: peter@reciprocitylabs.com
# Maintained By: peter@reciprocitylabs.com

"""A module containing the implementation of the assessment template entity."""

import json

from sqlalchemy.orm import validates

from ggrc import db
from ggrc.models.reflection import AttributeInfo
from ggrc.models.exceptions import ValidationError
from ggrc.models.mixins import Base
from ggrc.models.mixins import Slugged
from ggrc.models.mixins import Titled
from ggrc.models.mixins import CustomAttributable
from ggrc.models.reflection import PublishOnly
from ggrc.models.relationship import Relatable
from ggrc.models.types import JsonType


class AssessmentTemplate(Slugged, Base, Relatable, Titled,
                         CustomAttributable, db.Model):
  """A class representing the assessment template entity.

  An Assessment Template is a template that allows users for easier creation of
  multiple Assessments that are somewhat similar to each other, avoiding the
  need to repeatedly define the same set of properties for every new Assessment
  object.
  """
  __tablename__ = "assessment_templates"
  _mandatory_default_people = ("assessors", "verifiers")

  # the type of the object under assessment
  template_object_type = db.Column(db.String, nullable=True)

  # whether to use the control test plan as a procedure
  test_plan_procedure = db.Column(db.Boolean, nullable=False, default=False)

  # procedure description
  procedure_description = db.Column(db.Text, nullable=True)

  # the people that should be assigned by default to each assessment created
  # within the releated audit
  default_people = db.Column(JsonType, nullable=False)

  # labels to show to the user in the UI for various default people values
  DEFAULT_PEOPLE_LABELS = {
      "Object Owners": "Object Owners",
      "Audit Lead": "Audit Lead",
      "Auditors": "Auditors",
      "Primary Assessor": "Principal Assessor",
      "Secondary Assessors": "Secondary Assessors",
      "Primary Contact": "Primary Contact",
      "Secondary Contact": "Secondary Contact",
  }

  _title_uniqueness = False

  # REST properties
  _publish_attrs = [
      "template_object_type",
      "test_plan_procedure",
      "procedure_description",
      "default_people",
      PublishOnly("DEFAULT_PEOPLE_LABELS")
  ]

  _aliases = {
      "audit": {
          "display_name": "Audit",
          "mandatory": True,
          "type": AttributeInfo.Type.MAPPING,
          "ignore_on_update": True,
      },
      "default_assessors": {
          "display_name": "Default Assessors",
          "mandatory": True,
      },
      "default_verifier": {
          "display_name": "Default Verifier",
          "mandatory": True,
      },
      "default_test_plan": "Default Test Plan",
      "test_plan_procedure": "Use Control Test Plan",
      "object_under_assessment": {
          "display_name": "Object Under Assessment",
          "mandatory": True,
      },

  }

  @classmethod
  def generate_slug_prefix_for(cls, obj):
    return "TEMPLATE"

  @validates('default_people')
  def validate_default_people(self, key, value):
    """Check that default people lists are not empty.

    Check if the default_people contains both assessors and verifiers. The
    values of those fields must be thruthy, and if the value is a string it
    must be a valid default people label. If the value is not a string, it
    should be a list of valid user ids, but that is too expensive to test in
    this validator.
    """
    # pylint: disable=unused-argument
    parsed = json.loads(value)
    for mandatory in self._mandatory_default_people:
      mandatory_value = parsed.get(mandatory)
      if (not mandatory_value or
              isinstance(mandatory_value, list) and
              any(not isinstance(p_id, int) for p_id in mandatory_value) or
              isinstance(mandatory_value, basestring) and
              mandatory_value not in self.DEFAULT_PEOPLE_LABELS):
        raise ValidationError(
            'Invalid value for default_people.{field}. Expected a people '
            'label in string or a list of int people ids, recieved {value}.'
            .format(field=mandatory, value=mandatory_value),
        )

    return value
