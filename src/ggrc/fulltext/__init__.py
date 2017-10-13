# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Fulltext init indexer mudule"""

from collections import defaultdict
from collections import Iterable

from sqlalchemy import event

from ggrc import db
from ggrc.extensions import get_extension_instance

ACTIONS = ['after_insert', 'after_delete', 'after_update']


class Indexer(object):
  """General class for indexer"""

  def __init__(self, settings):
    self.indexer_rules = defaultdict(list)
    self.cache = defaultdict(dict)
    self.builders = {}

  def get_builder(self, obj_class):
    """return recordbuilder for sent class

    save it in builders dict arguments and cache it here
    """
    builder = self.builders.get(obj_class.__name__)
    if builder is not None:
      return builder
    from ggrc.fulltext import recordbuilder
    builder = recordbuilder.RecordBuilder(obj_class, self)
    self.builders[obj_class.__name__] = builder
    return builder

  def fts_record_for(self, obj):
    return self.get_builder(obj.__class__).as_record(obj)

  def invalidate_cache(self):
    self.cache = defaultdict(dict)

  def create_record(self, record):
    raise NotImplementedError()

  def update_record(self, record):
    raise NotImplementedError()

  def delete_record(self, key):
    raise NotImplementedError()

  def search(self, terms):
    raise NotImplementedError()


def resolve_default_text_indexer():
  """Get indexer for settings fulltest db"""
  from ggrc import settings
  db_scheme = settings.SQLALCHEMY_DATABASE_URI.split(':')[0].split('+')[0]
  return 'ggrc.fulltext.{db_scheme}.Indexer'.format(db_scheme=db_scheme)


def get_indexer():
  return get_extension_instance(
      'FULLTEXT_INDEXER', resolve_default_text_indexer)


def _runner(mapper, content, target):  # pylint:disable=unused-argument
  """Collect all reindex models in session"""
  import ggrc.fulltext
  from ggrc.fulltext.mixin import Indexed
  ggrc_indexer = ggrc.fulltext.get_indexer()
  db.session.reindex_set = getattr(db.session, "reindex_set", set())
  getters = ggrc_indexer.indexer_rules.get(target.__class__.__name__) or []
  for getter in getters:
    to_index_list = getter(target)
    if not isinstance(to_index_list, Iterable):
      to_index_list = [to_index_list]
    for to_index in to_index_list:
      db.session.reindex_set.add(to_index)
  if isinstance(target, Indexed):
    db.session.reindex_set.add(target)


def init_indexer():
  """Indexing initialization procedure"""
  import ggrc.fulltext
  from ggrc.fulltext.mixin import Indexed
  from ggrc.models import all_models
  ggrc_indexer = ggrc.fulltext.get_indexer()

  for model in all_models.all_models:
    for action in ACTIONS:
      event.listen(model, action, _runner)
    if not issubclass(model, Indexed):
      continue
    for sub_model in model.mro():
      for rule in getattr(sub_model, "AUTO_REINDEX_RULES", []):
        ggrc_indexer.indexer_rules[rule.model].append(rule.rule)
