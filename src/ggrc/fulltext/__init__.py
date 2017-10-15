# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Fulltext init indexer mudule"""

from collections import Iterable

from sqlalchemy import event

from ggrc import db
from ggrc.extensions import get_extension_instance

ACTIONS = ['after_insert', 'after_delete', 'after_update']


def get_indexer():
  """Get mysql indexer.

  This is a weird way of getting a MysqlIndexer "singleton". The indexer should
  be moved its own module and used without a class, and then this function
  should be removed.
  """
  return get_extension_instance(
      "FULLTEXT_INDEXER", "ggrc.fulltext.mysql.MysqlIndexer")


def _runner(mapper, content, target):  # pylint:disable=unused-argument
  """Collect all reindex models in session"""
  from ggrc.fulltext.mixin import Indexed
  ggrc_indexer = get_indexer()
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


def register_fulltext_listeners():
  """Indexing initialization procedure"""
  from ggrc.fulltext.mixin import Indexed
  from ggrc.models import all_models
  ggrc_indexer = get_indexer()

  for model in all_models.all_models:
    for action in ACTIONS:
      event.listen(model, action, _runner)
    if not issubclass(model, Indexed):
      continue
    for sub_model in model.mro():
      for rule in getattr(sub_model, "AUTO_REINDEX_RULES", []):
        ggrc_indexer.indexer_rules[rule.model].append(rule.rule)
