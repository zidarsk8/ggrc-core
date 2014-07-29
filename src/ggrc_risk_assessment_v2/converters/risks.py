# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com

from ggrc.converters.base import *
from ggrc.models.all_models import OrgGroup, Person, Relationship
from ggrc.models.mixins import BusinessObject
from ggrc.converters.base_row import *
from ggrc_risk_assessment_v2.models import Risk
from ggrc_risk_assessment_v2.converters.base_row import *
from collections import OrderedDict

class RiskRowConverter(BaseRowConverter):
  model_class = Risk

  def find_by_slug(self, slug):
    return Risk.query.filter_by(slug=slug).first()

  def setup_object(self):
    self.obj = self.setup_object_by_slug(self.attrs)
    if self.obj.id:
      self.add_warning('slug', "Risk already exists and will be updated")

  def reify(self):
    self.handle('slug', SlugColumnHandler)
    self.handle_title('title', is_required=True)
    self.handle_text_or_html('description')
    self.handle('contact', ContactEmailHandler, person_must_exist=True)
    self.handle('objects', RiskObjectsHandler)
    # Owner is more complicated; hold off on first iteration
    #self.handle('owners', ContactEmailHandler, person_must_exist=True, is_required=True)

  def save_object(self, db_session, **options):
    db_session.add(self.obj)


class RiskConverter(BaseConverter):

  metadata_export_order = ['type', 'slug']


  metadata_map = OrderedDict([
    ('Type','type')
  ])

  object_export_order = [
    'slug', 'title', 'description', 'notes',
    'controls', 'created_at', 'updated_at'
  ]

  object_map = OrderedDict([
    ('Risk Code', 'slug'),
    ('Title', 'title'),
    ('Description' , 'description'),
    ('Map:Person of Contact', 'contact'),
    ('Map:Objects', 'objects'),
  ])

  row_converter = RiskRowConverter

  def do_export_metadata(self):
    yield self.metadata_map.keys()
    yield ['Risks']
    yield []
    yield []
    yield self.object_map.keys()
