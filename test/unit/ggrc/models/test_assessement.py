# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: samo@reciprocitylabs.com
# Maintained By: samo@reciprocitylabs.com

""" Unit tests for the Assessment object """

from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ggrc import db
from ggrc.models import mixins
from ggrc.models import Assessment
from ggrc.models.object_document import Documentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState

from unit.ggrc.models.base_mixins import BaseMixins


class TestAssessmentMixins(BaseMixins):
  """ Tests inclusion of correct mixins and their attributes """

  def setUp(self):
    self.model = Assessment
    self.included_mixins = [
        mixins.Assignable,
        mixins.BusinessObject,
        mixins.CustomAttributable,
        db.Model,
        Documentable,
        HasObjectState,
        mixins.TestPlanned,
        mixins.Timeboxed,
        Ownable,
        Personable,
        Relatable,
    ]

    self.attributes_introduced = [
        ('audit', dict),
        ('design', InstrumentedAttribute),
        ('operationally', InstrumentedAttribute),
        ('object', dict),
        ('status', InstrumentedAttribute),                    # Stateful
        ('assignees', property),                              # Assignable
        ('contact_id', InstrumentedAttribute),                # WithContact
        ('contact', InstrumentedAttribute),                   # WithContact
        ('secondary_contact', InstrumentedAttribute),         # WithContact
        ('custom_attribute_values', InstrumentedAttribute),   # CustomAttrib.
        ('description', InstrumentedAttribute),               # Described
        ('end_date', InstrumentedAttribute),                  # Timeboxed
        ('notes', InstrumentedAttribute),                     # Noted
        ('object_documents', InstrumentedAttribute),          # Documentable
        ('object_people', InstrumentedAttribute),             # Personable
        ('os_state', InstrumentedAttribute),                  # HasObjectState
        ('owners', AssociationProxy),                         # Ownable
        ('reference_url', InstrumentedAttribute),             # HyperLinked
        ('related_sources', InstrumentedAttribute),           # Relatable
        ('related_destinations', InstrumentedAttribute),      # Relatable
        ('revisions', InstrumentedAttribute),                 # Revisionable
        ('slug', InstrumentedAttribute),                      # Slugged
        ('start_date', InstrumentedAttribute),                # Timeboxed
        ('test_plan', InstrumentedAttribute),                 # TestPlanned
        ('title', InstrumentedAttribute),                     # Titled
        ('url', InstrumentedAttribute),                       # HyperLinked
    ]
