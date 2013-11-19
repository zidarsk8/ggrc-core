# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from .base import *
from ggrc.models import Directive, Policy, Regulation, Contract, Standard, Objective, ObjectObjective
from .base_row import *
from collections import OrderedDict

DIRECTIVE_CLASSES = [Directive, Policy, Regulation, Contract, Standard]

class ObjectiveRowConverter(BaseRowConverter):
  model_class = Objective

  def find_by_slug(self, slug):
    from sqlalchemy import orm
    return self.model_class.query.filter_by(slug=slug).options(
        orm.joinedload('directive_controls')).first()

  def setup_object(self):
    self.obj = self.setup_object_by_slug(self.attrs)
    if self.obj.id is not None:
      self.add_warning('slug', "Objective already exists and will be updated")

  def reify(self):
    self.handle('slug', SlugColumnHandler)
    self.handle_date('start_date')
    self.handle_date('end_date')
    self.handle_date('created_at', no_import=True)
    self.handle_date('updated_at', no_import=True)
    self.handle_text_or_html('description')

    self.handle_raw_attr('title', is_required=True)
    self.handle_raw_attr('url')

    self.handle_option('kind', role='control_kind')
    self.handle_option('means', role='control_means')
    self.handle_option('verify_frequency')

    self.handle_boolean('key_control', truthy_values=['key', 'key_control',
                        'key control'], no_values=[])
    fraud_truthy = ['fraud', 'fraud_related', 'fraud related']
    fraud_falses = ['not fraud', 'not_fraud','not fraud_related', 'not fraud related']
    self.handle_boolean('fraud_related', truthy_values=fraud_truthy,
      no_values=fraud_falses)
    self.handle_boolean('active', truthy_values = ['active'], no_values = [])

    self.handle('documents', LinkDocumentsHandler)
    self.handle('categories', LinkControlCategoriesHandler)
    self.handle('assertions', LinkControlAssertionsHandler)
    self.handle('owner', ContactEmailHandler, person_must_exist=True)
    self.handle('systems', LinkObjectControl, model_class = System)
    self.handle('processes', LinkObjectControl, model_class = Process)

  def save_object(self, db_session, **options):
    #if options.get('directive_id'):
    db_session.add(self.obj)

  def after_save(self, db_session, **options):
    if options.get('parent_type') in DIRECTIVE_CLASSES:
      directive_id = options.get('parent_id')
      for directive_control in self.obj.directive_controls:
        if directive_control.directive_id == directive_id:
          return
      db_session.add(
          ObjectObjective(directive_id=directive_id, objective=self.obj))


class ObjectivesConverter(BaseConverter):

  metadata_map = OrderedDict([
    ('Type', 'type'),
    ('Directive Code', 'slug')
  ])

  object_map = OrderedDict([
    ('Control Code', 'slug'),
    ('Title', 'title'),
    ('Description', 'description'),
    ('Kind', 'kind'),
    ('Means', 'means'),
    ('Version', 'version'),
    ('Start Date', 'start_date'),
    ('Stop Date', 'end_date'),
    ('URL', 'url'),
    ('Map:Systems', 'systems'),
    ('Map:Processes', 'processes'),
    ('Map:Categories', 'categories'),
    ('Map:Assertions', 'assertions'),
    ('Frequency', 'verify_frequency'),
    ('Link:References', 'documents'),
    ('Map:Person of Contact', 'owner'),
    ('Key Control', 'key_control'),
    ('Active', 'active'),
    ('Fraud Related', 'fraud_related'),
    ('Created', 'created_at'),
    ('Updated' ,'updated_at')
  ])

  row_converter = ObjectiveRowConverter

  def validate_code(self, attrs):
    if not attrs.get('slug'):
      self.errors.append('Missing {} Code heading'.format(self.parent_type_string()))
    elif attrs['slug'] != self.parent_object().slug:
      self.errors.append('{0} Code must be {1}'.format(
          self.parent_type_string(),
          self.parent_object().slug
      ))

  # Creates the correct metadata_map for the specific directive kind.
  def create_metadata_map(self):
    parent_type = self.options.get('parent_type')
    if parent_type in DIRECTIVE_CLASSES:
      self.metadata_map = OrderedDict( [(k.replace("Directive", self.directive_kind()), v) \
                          if 'Directive' in k else (k, v) for k, v in self.metadata_map.items()] )

  def validate_metadata(self, attrs):
    self.validate_metadata_type(attrs, "Controls")
    self.validate_code(attrs)

  def parent_object(self):
    parent_type = self.options['parent_type']
    return parent_type.query.get(self.options['parent_id'])

  def parent_type_string(self):
    return self.options.get('parent_type').__name__

  def directive_kind(self):
    parent_object = self.parent_object()
    return parent_object.meta_kind

  def do_export_metadata(self):
    yield self.metadata_map.keys()
    yield ['Controls', self.parent_object().slug]
    yield[]
    yield[]
    yield self.object_map.keys()

