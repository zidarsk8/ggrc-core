# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from flask import Flask
from flask.ext.jasmine import Asset
from flask.ext.jasmine import Jasmine
from flask.ext.sqlalchemy import get_debug_queries

from ggrc import contributions  # noqa: imported so it can be used with getattr
from ggrc import db
from ggrc import extensions
from ggrc import settings


app = Flask('ggrc', instance_relative_config=True)
app.config.from_object(settings)
if "public_config" not in app.config:
  app.config.public_config = {}

for key in settings.exports:
  app.config.public_config[key] = app.config[key]


# Configure Flask-SQLAlchemy for app
db.app = app
db.init_app(app)


if getattr(settings, "FLASK_DEBUGTOOLBAR", False):
  from flask_debugtoolbar import DebugToolbarExtension
  toolbar = DebugToolbarExtension(app)


@app.before_request
def _ensure_session_teardown(*args, **kwargs):
  """Ensure db.session is correctly removed

  Occasionally requests are terminated without calling the teardown methods,
  namely with DeadlineExceededError on App Engine.
  """
  if db.session.registry.has():
    db.session.remove()


# Initialize models
import ggrc.models  # noqa
ggrc.models.init_app(app)

# Configure Flask-Login
import ggrc.login  # noqa
ggrc.login.init_app(app)

# Configure webassets for app
from ggrc import assets  # noqa
app.jinja_env.add_extension('webassets.ext.jinja2.assets')
app.jinja_env.assets_environment = assets.environment

# Configure Jinja2 extensions for app
app.jinja_env.add_extension('jinja2.ext.autoescape')
app.jinja_env.autoescape = True
app.jinja_env.add_extension('jinja2.ext.with_')
app.jinja_env.add_extension('hamlpy.ext.HamlPyExtension')

# Initialize services
import ggrc.services  # noqa
ggrc.services.init_all_services(app)

# Initialize views
import ggrc.views  # noqa
ggrc.views.init_all_views(app)

# Initialize extension blueprints
for extension_module in extensions.get_extension_modules():
  if hasattr(extension_module, 'blueprint'):
    app.register_blueprint(extension_module.blueprint)

# Initialize configured and default extensions
from ggrc.fulltext import get_indexer  # noqa
ggrc.indexer = get_indexer()

from ggrc.rbac import permissions  # noqa
permissions.get_permissions_provider()

from ggrc.automapper import register_automapping_listeners  # noqa
register_automapping_listeners()

if settings.ENABLE_JASMINE:
  # Configure Flask-Jasmine, for dev mode unit testing
  jasmine = Jasmine(app)

  jasmine.sources(
      Asset("dashboard-js"),
      Asset("dashboard-js-spec-helpers"),
      Asset("dashboard-js-templates"))

  jasmine.specs(
      Asset("dashboard-js-specs"))

if hasattr(settings, 'SQLALCHEMY_RECORD_QUERIES')\
        and settings.SQLALCHEMY_RECORD_QUERIES:

  def with_prefix(statement, prefix):
    return "\n".join([prefix + line for line in statement.splitlines()])

  @app.after_request
  def display_queries(response):
    queries = get_debug_queries()
    for query in queries:
      app.logger.info("{:.8f} {}\n{}".format(
          query.duration,
          query.context,
          with_prefix(query.statement, "       ")))
    app.logger.info("Total queries: {}".format(len(queries)))
    return response
