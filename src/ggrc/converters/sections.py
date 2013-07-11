from .base import *

from ggrc.models import Directive, Section
from .import_helper import *
from .base_row import *

class SectionRowConverter(BaseRowConverter):

  model_class = Section

  def setup_object(self):
    obj = self.setup_object_by_slug(self.attrs)
    if obj.directive \
        and obj.directive is not self.converter.options.get('directive'):
      self.add_error('slug', "Code is used in {0}: {1}".format(
        obj.directive.meta_kind,
        obj.directive.slug
        ))
    else:
      obj.directive = self.importer.options.get('directive')

  def reify(self):
    self.handle('slug', SlugColumnHandler)
    self.handle_date('created_at', no_import = True)
    self.handle_date('updated_at', no_import = True)
    self.handle_text_or_html('description')
    self.handle_text_or_html('notes')
    self.handle('controls', LinkControlsHandler)
    self.handle_raw_attr('title')

    return [str(self.obj.slug),str(self.obj.title), str(self.obj.description), str(self.obj.notes)]


class SectionsConverter(BaseConverter):
  metadata_export_order = ['type', 'slug']

  metadata_map = {
    'Type' : 'type',
    'Section Code'  : 'slug',
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

  # FIXME: Temporary as I test import from the command line
  @classmethod
  def start_import(cls, filepath, **options):
    return handle_csv_import(cls, filepath, **options)

if __name__ == '__main__':
  import sys
  if sys.argv[1] == 'import' and sys.argv[2] != None:
    SectionsConverter.start_import(sys.argv[2],)

