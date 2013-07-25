from .base import *

from ggrc.models.all_models import System, OrgGroup
from .base_row import *
from collections import OrderedDict

class SystemRowConverter(BaseRowConverter):
  model_class = System

  def setup_object(self):
    self.obj = self.setup_object_by_slug(self.attrs)
    self.obj.is_biz_process = self.importer.options.get('is_biz_process', False)

  def reify(self):
    self.handle('slug', SlugColumnHandler)
    self.handle('controls', LinkControlsHandler)
    self.handle('people_responsible', LinkPeopleHandler, role = 'responsible')
    self.handle('people_accountable', LinkPeopleHandler, role = 'accountable')
    self.handle('documents', LinkDocumentsHandler)
    self.handle('sub_systems', LinkSystemsHandler, is_biz_process = False)
    self.handle('sub_processes', LinkSystemsHandler, association = 'sub_systems',
                is_biz_process = True)
    self.handle_option('network_zone')
    self.handle('org_groups', LinkRelationshipsHandler, model_class = OrgGroup,
                relationship_type_id = 'org_group_is_responsible_for_system')
    self.handle_date('start_date')
    self.handle_date('created_at', no_import = True)
    self.handle_date('updated_at', no_import = True)
    self.handle_text_or_html('description')
    self.handle_boolean('infrastructure', truthy_values = ['infrastructure'])
    self.handle_raw_attr('title')

  def save_object(self, db_session, **options):
    db_session.add(self.obj)


class SystemsConverter(BaseConverter):

  metadata_export_order = ['type', 'slug']


  metadata_map = OrderedDict([
    ('Type','type')
  ])

  object_export_order = [
    'slug', 'title', 'description', 'notes',
    'controls', 'created_at', 'updated_at'
  ]

  object_map = OrderedDict([
    ('System Code', 'slug'),
    ('Title', 'title'),
    ('Description' , 'description'),
    ('Link:References', 'documents'),
    ('Infrastructure', 'infrastructure'),
    ('Link:People;Responsible', 'people_responsible'),
    ('Link:People;Accountable', 'people_accountable'),
    ('Link:Controls', 'controls'),
    ('Link:System;Sub System', 'sub_systems'),
    ('Link:Process;Sub Process', 'sub_processes'),
    ('Link:Org Group;Overseen By', 'org_groups'),
    ('Effective Date', 'start_date'),
    ('Created', 'created_at'),
    ('Updated', 'updated_at'),
    ('Network Zone', 'network_zone')
  ])

  row_converter = SystemRowConverter

  def create_object_map(self):
    if self.options.get('is_biz_process'):
      self.object_map = OrderedDict( [(k.replace("System Code", 'Process Code'), v) \
                        if k == 'System Code' else (k, v) for k, v in self.object_map.items()] )

  def do_export_metadata(self):
    yield self.metadata_map.keys()
    yield ['Processes' if self.options.get('is_biz_process') else 'Systems']
    yield []
    yield []
    yield self.object_map.keys()
