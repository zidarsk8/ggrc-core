
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from .all_models import *

"""All gGRC model objects and associated utilities."""

def create_db_with_create_all():
  from ggrc.app import db
  import ggrc.models.all_models
  db.create_all()

def create_db_with_migrations(quiet=False):
  from ggrc.app import db
  from ggrc.migrate import upgradeall
  import logging
  if quiet:
    logging.disable(logging.INFO)
  upgradeall()
  if quiet:
    logging.disable(logging.NOTSET)

def drop_db_with_drop_all():
  from ggrc.app import db
  import ggrc.models.all_models
  db.drop_all()

def drop_db_with_migrations(quiet=False):
  from ggrc.app import db
  from ggrc.migrate import downgradeall
  import ggrc.models.all_models
  import logging
  from ggrc import settings
  if quiet:
    logging.disable(logging.INFO)
  if 'mysql' in settings.SQLALCHEMY_DATABASE_URI:
    db.engine.execute('SET FOREIGN_KEY_CHECKS = 0')
  downgradeall(drop_versions_table=True)
  if quiet:
    logging.disable(logging.NOTSET)
  db.drop_all()
  db.session.commit()
  if 'mysql' in settings.SQLALCHEMY_DATABASE_URI:
    db.engine.execute('SET FOREIGN_KEY_CHECKS = 1')

def create_db(use_migrations=False, quiet=False):
  if use_migrations:
    create_db_with_migrations(quiet)
  else:
    create_db_with_create_all()

def drop_db(use_migrations=False, quiet=False):
  if use_migrations:
    drop_db_with_migrations(quiet)
  else:
    drop_db_with_drop_all()

def init_app(app):
  from .all_models import all_models
  [model._inflector for model in all_models]

from .inflector import get_model
