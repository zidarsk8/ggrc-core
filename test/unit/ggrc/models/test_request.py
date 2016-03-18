# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: samo@reciprocitylabs.com
# Maintained By: samo@reciprocitylabs.com

""" Unit tests for the Request object """

from sqlalchemy.orm.attributes import InstrumentedAttribute
import unittest

from ggrc import db
from ggrc.models import mixins
from ggrc.models import Request
from ggrc.models.computed_property import computed_property
from ggrc.models.object_document import Documentable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable


class TestRequestMixins(unittest.TestCase):
  """ Tests inclusion of correct mixins and their attributes """

  def setUp(self):
    self.included_mixins = [
        mixins.Assignable,
        mixins.Base,
        mixins.CustomAttributable,
        mixins.Described,
        db.Model,
        Documentable,
        Personable,
        Relatable,
        mixins.Revisionable,
        mixins.Slugged,
        mixins.Titled,
    ]

    self.attributes_introduced = [
        ('assignees', property),                             # Assignable
        ('audit_id', InstrumentedAttribute),
        ('audit_object_id', InstrumentedAttribute),
        ('custom_attribute_values', InstrumentedAttribute),  # CustomAttrib.
        ('description', InstrumentedAttribute),              # Described
        ('display_name', computed_property),                 # Base
        ('due_on', InstrumentedAttribute),
        ('gdrive_upload_path', InstrumentedAttribute),
        ('notes', InstrumentedAttribute),
        ('object_documents', InstrumentedAttribute),         # Documentable
        ('object_people', InstrumentedAttribute),            # Personable
        ('related_sources', InstrumentedAttribute),          # Relatable
        ('related_destinations', InstrumentedAttribute),     # Relatable
        ('request_type', InstrumentedAttribute),
        ('requested_on', InstrumentedAttribute),
        ('requestor', InstrumentedAttribute),
        ('requestor_id', InstrumentedAttribute),
        ('responses', InstrumentedAttribute),
        ('revisions', InstrumentedAttribute),                # Revisionable
        ('slug', InstrumentedAttribute),                     # Slugged
        ('status', InstrumentedAttribute),
        ('test', InstrumentedAttribute),
        ('title', InstrumentedAttribute),                    # Titled
    ]

  def test_includes_correct_mixins(self):
    for mixin in self.included_mixins:
      self.assertTrue(
          issubclass(Request, mixin),
          'Expected Request to inherit from {} but it does not'.format(mixin)
      )

  def test_correct_attrs_introduced(self):
    for attr_name, expected_type in self.attributes_introduced:
      actual_type = type(getattr(Request, attr_name))
      self.assertEqual(
          expected_type,
          actual_type,
          'Expected attr "{}" to be of type {} but is actually {}'
          .format(attr_name, expected_type, actual_type)
      )
