from .base import *

from ggrc.models import Directive, Section
from .import_helper import *
from .base_row import *

class SectionRowConverter(BaseRowConverter):
  model_class = Section

  def setup_object(self):
    self.obj = self.setup_object_by_slug(self.attrs)
    if self.obj.directive \
        and self.obj.directive is not self.importer.options.get('directive'):
          self.importer.errors.append('Slug code is already used.')
    else:
      self.obj.directive = self.importer.options.get('directive')

  def reify(self):
    self.handle('slug', SlugColumnHandler)
    self.handle_date('created_at', no_import = True)
    self.handle_date('updated_at', no_import = True)
    self.handle_text_or_html('description')
    self.handle_text_or_html('notes')
    self.handle('controls', LinkControlsHandler)
    self.handle_raw_attr('title')

    return [str(self.obj.slug),str(self.obj.title), str(self.obj.description), str(self.obj.notes)]

  def save_object(self, db_session, **options):
    if options.get('directive_id'):
      self.obj.directive_id = int(options.get('directive_id'))
      db_session.add(self.obj)


class SectionsConverter(BaseConverter):

  metadata_export_order = ['type', 'slug']

  metadata_map = {
    'Type' : 'type',
    'Regulation Code'  : 'slug',
    'Section Title' : 'title',
    'Section Description' : 'description',
    'Version' : 'version',
    'Start'   : 'start_date',
    'Stop'    : 'stop_date',
    'Kind'    : 'kind',
    'Audit Start' : 'audit_start_date',
    'Audit Frequency' : 'audit_frequency',
    'Audit Duration'  : 'audit_duration',
    'Created' : 'created_at',
    'Updated' : 'updated_at'
  }

  object_export_order = [
    'slug', 'title', 'description', 'notes',
    'controls', 'created_at', 'updated_at'
    ]

  object_map = {
    'Section Code' : 'slug',
    'Section Title': 'title',
    'Section Description' : 'description',
    'Section Notes' : 'notes',
    'Created'  : 'created_at',
    'Updated'  : 'updated_at'
  }

  row_converter = SectionRowConverter

  def directive(self):
    return self.options['directive']

  @classmethod
  def start_import(cls, filepath, **options):
    return handle_csv_import(cls, filepath, **options)

