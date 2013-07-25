from .common import *
from ggrc.models.all_models import *

base_errors = []
errors = {}
base_warnings = []
warnings = {}
base_messages = []
messages = {}

def add_error(key, message = None):
  errors.setdefault(key, []).append(message)

def add_warning(key, message = None):
  warnings.setdefault(key, []).append(message)

# BaseRowConverter is the super class for SectionsRowConverter
class BaseRowConverter(object):

  def __init__(self, importer, object_or_attrs, index, **options):
    self.options = options if options else {}
    self.importer = importer
    self.index = index
    if self.options.get('export'):
      self.obj = object_or_attrs
      self.attrs = {}
    else:
      self.attrs = object_or_attrs if object_or_attrs else {}
      self.obj = None

    self.handlers = {}
    self.after_save_hooks = []

  def errors_for(self, key):
    error_messages = []
    if self.handlers.get(key) and self.handlers[key].errors:
      error_messages += self.handlers[key].errors
    error_messages += errors.get(key, []) + (self.obj.errors.get(key,[]) if self.obj else [])
    return error_messages

  def warnings_for(self, key):
    warning_messages = []
    if self.handlers.get(key) and self.handlers[key].warnings:
      warning_messages  += self.handlers[key].warnings
    warning_messages += errors.get(key, []) + (self.obj.errors.get(key,[]) if self.obj else [])
    return warning_messages

  def has_errors(self):
    return any(errors) or any([val.errors for val in self.handlers.values()])

  def has_warnings(self):
    return any(warnings) or any([val.warnings for val in self.handlers.values()])

  def setup(self):
    pass

  #FIXME: changed_attributes on rails side needs to be converted
  def changed_attributes(self):
    pass

  def __getitem__(self, key):
    return self.handlers[key]

  def setup(self):
    if self.options.get('export'):
      self.setup_export()
    else:
      self.clean_attrs()
      self.setup_object()

  def setup_export(self):
    self.attrs['slug'] = self.obj.slug

  def clean_attrs(self):
    for k in self.attrs:
      self.attrs[k] = self.attrs[k].strip() if isinstance(self.attrs[k],basestring) else ''

  def setup_object(self):
    self.setup_object_by_slug(self.attrs)

  def setup_object_by_slug(self, attrs):
    slug = prepare_slug(attrs['slug']) if attrs.get('slug') else ''
    if not slug:
      self.obj = self.model_class()
    else:
      self.obj = self.find_by_slug(slug)
      self.obj = self.obj if self.obj else self.importer.find_object(self.model_class, slug)
      self.obj = self.obj if self.obj else self.model_class()
      self.obj.slug = slug
    self.importer.add_object(self.model_class, slug, self.obj)
    return self.obj

  def add_after_save_hook(self, hook = None, funct = None):
    if hook: self.after_save_hooks.append(hook)
    if funct and callable(funct): self.after_save_hooks.append(funct)

  def responds_to_after_save(hook):
    if hasattr(hook, 'after_save'):
      return callable(getattr(hook, 'after_save'))
    return False

  def run_after_save_hooks(self, obj):
    for hook in self.after_save_hooks:
      if responds_to_after_save(hook):
        hook.after_save(obj)
      elif callable(hook):
        hook(obj)
      elif isinstance(hook, basestring):
        self.hook(obj)
      else:
        raise ImportException

  def handle_boolean(self, key, **options):
    return self.handle(key, BooleanColumnHandler, **options)

  def handle_text_or_html(self, key, **options):
    return self.handle(key, TextOrHtmlColumnHandler, **options)

  def handle_raw_attr(self, key, **options):
    return self.handle(key, ColumnHandler, **options)

  def handle_date(self, key, **options):
    self.handle(key, DateColumnHandler, **options)

  def handle_option(self, key, **options):
    self.handle(key, OptionColumnHandler, **options)

  def find_by_slug(self, slug):
    return self.model_class.query.filter_by(slug=str(slug)).first()

  def set_attr(self, name, value):
    setattr(self.obj, name, value)

  def get_attr(self, name):
    return getattr(self.obj, name, '') or ''

  def handle(self, key, handler_class, **options):
    self.handlers[key] = handler_class(self, key, **options)
    if self.options.get('export'):
      self.attrs[key] =  self.handlers[key].export()
    else:
      handle_result = self.handlers[key].do_import(self.attrs.get(key))
      #self.add_after_save_hook(self.handlers[key])
      return handle_result

class ColumnHandler(object):

  def __init__(self, importer, key, **options):
    options.setdefault('no_import', False)
    self.importer = importer
    self.key = key
    self.options = options

    self.original = None
    self.value = None

    self.errors = []
    self.warnings = []

  def add_error(self, message):
    self.errors.append(message)

  def add_warning(self, message):
    self.warnings.append(message)

  def has_error(self):
    return any(self.errors) or self.importer.errors.get(self.key) or self.importer.obj.errors.get(self.key)

  def has_warnings(self):
    return any(self.warnings) or self.importer.warnings.get(self.key)

  def display(self):
    return getattr(self.importer.obj, key)

  def after_save(self, obj):
    pass

  def parse_item(self, value):
    return value

  def validate(self, data):
    pass

  def do_import(self, content):
    self.original = content
    if not self.options.get('no_import'):
      return self.go_import(content)

  def go_import(self, content):
    if content:
      data = self.parse_item(content)
      self.validate(data)
      if data:
        self.value = data
        self.set_attr(data)
      return data
    return ''

  def set_attr(self, value):
    self.importer.set_attr(self.key, value)

  def export(self):
    return getattr(self.importer.obj, self.key)


class TextOrHtmlColumnHandler(ColumnHandler):

  def parse_item(self, value):
    if value:
      value = value.strip()
      if not isinstance(value, unicode):
        value = value.encode('utf-8')
        value = unicode(value, 'utf-8')
    return value or ''

class SlugColumnHandler(ColumnHandler):

  # Dont overwrite slug on object
  def go_import(self, content):
    if content:
      self.value = content
      if self.value in self.importer.importer.get_slugs():
        self.add_error('Slug Code is duplicated in CSV')
      else:
        self.importer.importer.add_slug_to_slugs(self.value)
      self.validate(content)
    else:
      self.add_warning('Code will be autofilled')
    return content

class OptionColumnHandler(ColumnHandler):
  def parse_item(self, value):
    pass

class BooleanColumnHandler(ColumnHandler):
  def parse_item(self, value):
    truthy_values = options.get('truthy_values', []) + ['yes', '1', 'true', 'y']
    if value:
      return value.lower() in truthy_values
    return None

class DateColumnHandler(ColumnHandler):

  def parse_item(self, value):
    try:
      date_result = None
      if isinstance(value, basestring) and re.match(r'\d{1,2}\/\d{1,2}\/\d{4}', value):
        from datetime import datetime
        date_result = datetime.strptime(value, "%m/%d/%Y")
      elif isinstance(value, basestring) and re.match(r'\d{1,2}\/\d{1,2}\/\d{2}', value):
        from datetime import datetime
        date_result = datetime.strptime(value, "%m/%d/%y")
      elif isinstance(value, basestring) and re.match(r'\d{4}\/\d{1,2}\/\d{2}', value):
        from datetime import datetime
        date_result = datetime.strptime(value, "%y/%m/%d")
      else:
        raise ValueError("Error parsing the date string")

      if date_result:
        import ipdb; ipdb.set_trace() ### XXX BREAKPOINT
        return "{year}-{month}-{day}".format(year=date_result.year,month=date_result.month,day=date_result.day)
      else:
        return ''
    except ValueError as e:
      self.warnings.append("{}, use YYYY-MM-DD or MM/DD/YYYY format".format(e.message))

  def display(self):
    if self.has_errors():
      return self.original
    else:
      return getattr(self.importer.obj, self.key) if self.importer.obj else ''

  def export(self):
    date_result = getattr(self.importer.obj, self.key, '')
    return "{year}-{month}-{day}".format(year=date_result.year,month=date_result.month,day=date_result.day) if date_result else ''

class LinksHandler(ColumnHandler):

  def __init__(self, importer, key, **options):
    options['association'] = key if not options.get('association') else options['association']
    options['append_only'] = True if not options.get('append_only') else options['append_only']
    super(LinksHandler, self).__init__(importer, key, **options)

    self.model_class = None
    self.pre_existing_links = None
    self.link_status = {}
    self.link_objects = {}
    self.link_index = 0
    self.link_values = {}
    self.link_errors = {}
    self.link_warnings = {}

  def add_link_error(self, message):
    self.link_errors.setdefault(self.link_index, []).append(message)

  def add_link_warning(self, message):
    self.link_warnings.setdefault(self.link_index, []).append(message)

  def add_created_link(self, obj):
    self.link_status[self.link_index] = 'created'
    self.link_objects[self.link_index] = obj

  def add_existing_link(self, obj):
    self.link_status[self.link_index] = 'existing'
    self.link_objects[self.link_index] = obj

  def has_errors(self):
    return any(self.errors) or any(self.link_errors.values)

  def has_warnings(self):
    return any(self.warnings) or any(self.link_warnings.values)

  def imported_links(self):
    keys = self.link_objects.keys()
    status = self.link_status
    created_or_existed = [index for index in keys if status[index] == 'created' or 'existing']
    return [self.link_objects[index] for index in created_or_existed]

  def created_links(self):
    created_indices = [index for index in self.link_objects.keys() if self.link_status[index] == 'created']
    return [self.link_objects[index] for index in created_indices]

  def display(self):
    return "XXX"

  def display_link(self, obj):
    return obj.title

  def links_with_details(self):
    pass

  def go_import(self, content):
    pass

  def split_cell(self, value):
    pass

  def model_class(self):
    pass

  @classmethod
  def model_class(cls):
    pass

  def get_where_params(self, data):
    pass

  def get_create_params(self, data):
    return data

  def find_existing_item(self, data):
    pass

  def create_item_warnings(self, obj, data):
    pass

  def get_existing_items(self):
    pass

  def export(self):
    pass

  def join_rendered_items(self, items):
    pass

  def render_item(self, item):
    pass

  def save_linked_objects(self):
    pass

  def after_save(self, obj):
    pass

class LinkControlsHandler(LinksHandler):

  model_class = Control

  def parse_item(self, data):
    return {'slug' : data.upper()}

  def create_item(data):
    pass

class LinkCategoriesHandler(LinksHandler):
  model_class = Category

  def parse_item(self, data):
    return { 'name':data }


class LinkDocumentsHandler(LinksHandler):
  model_class = Document

  def parse_item(self, value):
    pass

class LinkPeopleHandler(LinksHandler):
  model_class = Person

  def parse_item(self, value):
    pass

class LinkSystemsHandler(LinksHandler):
  model_class = System

  def parse_item(self, value):
    pass

class LinkRelationshipsHandler(LinksHandler):

  def parse_item(self, value):
    pass



