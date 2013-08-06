from .common import *
#FIXME: Remove import of all model classes while we import
from ggrc.models.all_models import *

def unpack_list(vals):
  result = []
  for ele in vals:
    if isinstance(ele, list):
      for inner in ele: result.append(inner)
    else:
      result.append(ele)
  return result

def clean_list(vals):
  result = []
  for res in vals:
    if '[' in res and  ']' in res:
      result.append(res[1:-1].strip())
    elif '[' in res:
      result.append(res[1:].strip())
    elif ']' in res:
      result.append(res[:-1].strip())
    else:
      result.append(res.strip())
  return result

def split_cell(value):
  lines = [val.strip() for val in value.splitlines() if val]
  non_flat = [clean_list(line.split(',')) if line[0] == '[' else line for line in lines]
  return unpack_list(non_flat)

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
    self.errors = {}
    self.warnings = {}
    self.messages = {}

  def errors_for(self, key):
    error_messages = []
    if self.handlers.get(key) and self.handlers[key].errors:
      error_messages += self.handlers[key].errors
    error_messages += self.errors.get(key, [])
    return error_messages

  def warnings_for(self, key):
    warning_messages = []
    if self.handlers.get(key) and self.handlers[key].has_warnings():
      warning_messages  += self.handlers[key].warnings
    warning_messages += self.errors.get(key, [])
    return warning_messages

  def has_errors(self):
    return any(self.errors) or any([val.errors for val in self.handlers.values()])

  def has_warnings(self):
    return any(self.warnings) or any([val.warnings for val in self.handlers.values()])

  def setup(self):
    pass

  #TODO: changed_attributes on rails side needs to be converted
  def changed_attributes(self):
    pass

  def __getitem__(self, key):
    # Return generic handler if requested one is unavailable
    return self.handlers.get(key, ColumnHandler(self,''))

  def setup(self):
    if self.options.get('export'):
      self.setup_export()
    else:
      self.clean_attrs()
      self.setup_object()

  def setup_export(self):
    self.attrs['slug'] = self.obj.slug
    self.options['export'] = True

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
      self.obj = self.obj or self.importer.find_object(self.model_class, slug)
      self.obj = self.obj or self.model_class()
      self.obj.slug = slug
    self.importer.add_object(self.model_class, slug, self.obj)
    return self.obj

  def save(self, db_session, **options):
    self.save_object(db_session, **self.options)
    self.run_after_save_hooks(self.obj)

  def add_after_save_hook(self, hook = None, funct = None):
    if hook: self.after_save_hooks.append(hook)
    if funct and callable(funct): self.after_save_hooks.append(funct)

  def run_after_save_hooks(self, obj):
    for hook in self.after_save_hooks:
      if self.responds_to_after_save(hook):
        hook.after_save(obj)
      elif callable(hook):
        hook(obj)
      elif isinstance(hook, basestring):
        self.hook(obj)
      else:
        raise ImportException

  def responds_to_after_save(self, hook):
    if hasattr(hook, 'after_save'):
      return callable(getattr(hook, 'after_save', None))
    return False

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
      self.handlers[key].do_import(self.attrs.get(key))
      self.add_after_save_hook(self.handlers[key])

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

  def has_errors(self):
    return any(self.errors) or self.importer.errors.get(self.key)

  def has_warnings(self):
    return any(self.warnings) or self.importer.warnings.get(self.key)

  def display(self):
    value = getattr(self.importer.obj, self.key, '') or ''
    return value if value != 'null' else '' # Some columns returning null strings - should show as ''

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
    return getattr(self.importer.obj, self.key, '')

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
  from ggrc.models.option import Option
  def parse_item(self, value):
    if value:
      role = self.options.get('role') or self.key
      option = Option.query.filter_by(role = role.lower(), title = value.lower()).first()
      if not option:
        self.warnings.append(
          'Unknown "{}" option "{}" -- create this option from the Admin Dashboard'.format(
            self.options.get('role'), value.lower()))
      return option

  def display(self):
    if self.has_errors():
      return self.original
    else:
      return self.value.title

class BooleanColumnHandler(ColumnHandler):
  def parse_item(self, value):
    truthy_values = self.options.get('truthy_values', []) + ['yes', '1', 'true', 'y']
    if value:
      return value.lower() in truthy_values
    return None

class DateColumnHandler(ColumnHandler):

  def parse_item(self, value):
    try:
      from datetime import datetime
      date_result = None
      if isinstance(value, basestring) and re.match(r'\d{1,2}\/\d{1,2}\/\d{4}', value):
        date_result = datetime.strptime(value, "%m/%d/%Y")
      elif isinstance(value, basestring) and re.match(r'\d{1,2}\/\d{1,2}\/\d{2}', value):
        date_result = datetime.strptime(value, "%m/%d/%y")
      elif isinstance(value, basestring) and re.match(r'\d{4}\/\d{1,2}\/\d{2}', value):
        date_result = datetime.strptime(value, "%y/%m/%d")
      else:
        raise ValueError("Error parsing the date string")

      if date_result:
        return "{year}-{month}-{day}".format(year=date_result.year,month=date_result.month,day=date_result.day)
      else:
        return ''
    except ValueError as e:
      self.warnings.append("{}, use YYYY-MM-DD or MM/DD/YYYY format".format(e.message))

  def display(self):
    if self.has_errors():
      return self.original
    else:
      return self.value or getattr(self.importer.obj, self.key, '') or ''

  def export(self):
    date_result = getattr(self.importer.obj, self.key, '')
    return "{year}-{month}-{day}".format(year=date_result.year,month=date_result.month,day=date_result.day) if date_result else ''

class LinksHandler(ColumnHandler):

  model_class = None

  def __init__(self, importer, key, **options):
    options['association'] = str(key) if not options.get('association') else options['association']
    options['append_only'] = options.get('append_only', True)
    super(LinksHandler, self).__init__(importer, key, **options)

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
    return any(self.errors) or any(self.link_errors.values())

  def has_warnings(self):
    return any(self.warnings) or any(self.link_warnings.values())

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
    details = []
    for index in self.link_values.keys():
      details.append([self.link_status.get(index,''), self.link_objects.get(index,''),
                      self.link_values.get(index,''), self.link_errors.get(index,''),
                      self.link_warnings.get(index,'')])
    return details

  def get_existing_items(self):
    return getattr(self.importer.obj, self.options.get('association'),[])

  def go_import(self, content):
    content = content or ""
    if self.importer.options.get('export') or not self.importer.obj.id:
      self.pre_existing_links = []
    else:
      self.pre_existing_links = self.get_existing_items()

    for i, value in enumerate(split_cell(content)):
      self.link_index = i
      self.link_values[self.link_index] = value
      data = self.parse_item(value)
      if not data: next

      linked_object = self.find_existing_item(data)

      if not linked_object:
        # New object
        linked_object = self.create_item(data)
        if linked_object:
          self.add_created_link(linked_object)
      else:
        if linked_object in self.pre_existing_links:
          # Existing object with existing relationship
          self.add_existing_link(linked_object)
        else:
          # Existing object with a new relationship
          self.add_created_link(linked_object)


  def model_class(self):
    model_class = self.options.get('model_class') or self.__class__.model_class
    model_class = model_class.__name__
    model_class = model_class.upper()
    return model_class

  #TODO: add model class method -> Perhaps return '' (or None)?

  def get_where_params(self, data):
    return dict({'slug': data.get('slug')}.items() + self.options.get(
                'extra_model_where_params', []))

  def get_create_params(self,data):
    return data

  def find_existing_item(self, data):
    where_params = self.get_where_params(data)
    model_class = getattr(self.__class__, 'model_class', None) or self.model_class
    return model_class.query.filter_by(**where_params).first()

  def create_item(self, data):
    where_params = self.get_where_params(data)
    obj = self.importer.importer.find_object(self.model_class, where_params.get('slug'))
    if not obj:
      create_params = self.get_create_params(data)
      obj = self.model_class()
      if create_params.get('slug'):
        obj.slug = create_params['slug']
      self.importer.importer.add_object(self.model_class, where_params.get('slug'), obj)
    self.create_item_warnings(obj, data)
    return obj

  def create_item_warnings(self, obj, data):
    self.add_link_warning("'{0}' will be created".format(data.get('slug')))

  def get_existing_items(self):
    return getattr(self.importer.obj, self.options.get('association'), None)

  def export(self):
    return self.join_rendered_items([self.render_item(item) for item in self.get_existing_items() if item])

  def join_rendered_items(self, items):
    return "\r\n".join(items)

  def render_item(self, item):
    return item.slug

  def save_linked_objects(self):
    success = True
    for link_object in self.created_links():
      success = self.save_link_obj(link_object, db.session) and success
    return success

  # TODO: Save a linked object in the event of it being created on import
  def save_link_obj(self, link_obj, db_session):
    return True

  def after_save(self, obj):
    if self.options.get('append_only'):
      # Save old links plus new links
      if self.save_linked_objects():
        #new_objects = self.created_links - self.get_existing_items()
        #updated_total = self.created_links() + self.get_existing_items()
        if hasattr(obj, self.options.get('association')):
          target_attr = getattr(obj, self.options['association'])
          target_attr.extend([item for item in self.created_links() if item not in self.get_existing_items()])
      else:
        self.add_error("Failed to save necessary objects")
    else:
      # Overwrite with only imported links
      if hasattr(obj, self.options.get('association')):
        setattr(obj, self.options.get('association'), self.imported_links())

class LinkControlsHandler(LinksHandler):

  model_class = Control

  def parse_item(self, data):
    return {'slug' : data.upper()}

  def create_item(self, data):
    self.add_link_warning("Control with code {} doesn't exist".format(data.get('slug', '')))
    return None

class LinkCategoriesHandler(LinksHandler):
  from ggrc.models.category import Category
  model_class = Category

  def parse_item(self, data):
    return { 'name' : data }

  def get_where_params(self, data):
    return {'name' : data.get('name'), 'scope_id' : self.options.get('scope_id')}

  def find_existing_item(self, data):
    items = self.model_class.query.filter_by(scope_id = self.options.get('scope_id'), name = data.get('name') ).all()

    if len(items) > 1:
      self.add_link_error('Multiple matches found for "{}"'.format(data.get('name')))
    else:
      return items[0]

  def create_item(self, data):
    self.add_link_warning('Unknown category "{}" -- add this category from the Admin Dashboard'.format(data.get('name')))

  def render_item(self, item):
    return item.name

  def display_link(self, obj):
    return obj.name

class LinkDocumentsHandler(LinksHandler):
  from ggrc.models.document import Document
  import re
  model_class = Document

  def parse_item(self, value):
    data = {}
    if value[0] == '[':
      prog = re.compile(r'^\[([^\s]+)(?:\s+([^\]]*))?\]([^$]*)$')
      result = prog.match(value.strip())
      if result:
        data = { 'link': result.group(1), 'title': result.group(2), 'description': result.group(3)}
      else:
        self.add_link_error('Invalid format: use "[www.yoururl.com Document] Title"')
    else:
      data = { 'link' : value.strip() }

    #TODO: Add link validation here later on
    data['link'] = data['link'].strip()
    return data

  def get_where_params(self, data):
    return {'link' : data.get('link')}

  def create_item_warnings(self, obj, data):
    self.add_link_warning('"{}" will be created'.format(data.get('title') or data.get('link')))

  def render_item(self, item):
    return "[{} {}] {}".format(item.link_url, item.title, item.description)

class LinkPeopleHandler(LinksHandler):
  from ggrc.models.person import Person
  from ggrc.models.all_models import ObjectPerson
  model_class = Person
  import re

  def parse_item(self, value):
    data = {}
    if value[0] == '[':
      prog = re.compile(r'^\[([\w\d-]+@[^\s\]]+)(?:\s+([^\]]+))?\]([^$]*)$')
      match = prog.match(value)
      if match:
        data = { 'email' : match.group(1), 'name' : match.group(3) }
      else:
        self.add_link_error('Invalid format')
    else:
      data = { 'email' : value }

    if data:
      return data #TODO: Provide email validation here

  def get_where_params(self, data):
    return { 'email' : data.get('email') }

  def get_create_params(self, data):
    return {'email' : data.get('email'), 'name' : data.get('name') }

  def create_item_warnings(self, obj, data):
    self.add_link_warning('"{}" will be created'.format(data.get('email')))

  def get_existing_items(self):
    where_params = {}
    where_params['role'] = self.options.get('role')
    where_params['personable_type'] = self.importer.obj.__class__.__name__
    object_people = ObjectPerson.query.filter_by(**where_params).all()
    objects = [obj.person for obj in object_people]
    return objects

  def after_save(self, obj):
    db_session = db.session
    for linked_object in self.created_links():
      db_session.add(linked_object)
      object_person = ObjectPerson()
      object_person.personable = self.importer.obj
      object_person.person = linked_object
      db_session.add(object_person)

  def render_item(self, item):
    return item.email

  def display_link(self, obj):
    return obj.email

class LinkSystemsHandler(LinksHandler):
  from ggrc.models.all_models import System
  model_class = System

  def parse_item(self, value):
    return { 'slug' : value.upper(), 'title' : value }

  def find_existing_item(self, data):
    system = System.query.filter_by(slug = data.get('slug')).first()
    if not system:
      sys_type = "Process" if self.options.get('is_biz_process') else "System"
      self.add_link_warning("{} with code {} doesn't exist".format(sys_type, data.get('slug', '')))
    else:
      if self.options.get('is_biz_process') and not system.is_biz_process:
        self.add_link_warning("That code is used by a System, and will not be linked")
      elif not self.options.get('is_biz_process') and system.is_biz_process:
        self.add_link_warning('That code is used by a Process, and will not be linked')
      else:
        return system

  def get_existing_items(self):
    where_params = { 'is_biz_process' : self.options.get('is_biz_process') or False }
    return System.query.filter_by(**where_params).all()

  def create_item(self, data):
    return None

class LinkRelationshipsHandler(LinksHandler):

  def parse_item(self, value):
    pass

