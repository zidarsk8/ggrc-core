# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

"""
Sets up Flask app
"""

from flask import Flask
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.sqlalchemy import SQLAlchemy
from tabulate import tabulate
from ggrc import contributions  # noqa: imported so it can be used with getattr
from ggrc import db
from ggrc import extensions
from ggrc import settings


app = Flask('ggrc', instance_relative_config=True)  # noqa: valid constant name
app.config.from_object(settings)
if "public_config" not in app.config:
  app.config.public_config = {}

for key in settings.exports:
  app.config.public_config[key] = app.config[key]


# Configure Flask-SQLAlchemy for app
db.app = app
db.init_app(app)


@app.before_request
def _ensure_session_teardown():
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


def _enable_debug_toolbar():
  """Enable flask debug toolbar for benchmarking requests."""
  if getattr(settings, "FLASK_DEBUGTOOLBAR", False):
    from flask_debugtoolbar import DebugToolbarExtension
    DebugToolbarExtension(app)


def _enable_jasmine():
  """Set jasmine sources and specs if it's enabled.

  Jasmine is used for javascript tests and is not installed on the production
  environment, that is why we must check if it enabled before tying to import
  it.
  """
  if getattr(settings, "ENABLE_JASMINE", False):
    from flask.ext.jasmine import Asset
    from flask.ext.jasmine import Jasmine
    # Configure Flask-Jasmine, for dev mode unit testing
    jasmine = Jasmine(app)

    jasmine.sources(
        Asset("dashboard-js"),
        Asset("dashboard-js-spec-helpers"),
        Asset("dashboard-js-templates"))

    jasmine.specs(
        Asset("dashboard-js-specs"))


def _display_sql_queries():
  """Set up display database queries

  This function makes sure we display the sql queries if the record setting is
  enabled.
  """
  if getattr(settings, "SQLALCHEMY_RECORD_QUERIES", False):
    @app.after_request
    def display_queries(response):  # noqa: not an unused variable
      """Display database queries

      Prints out SQL queries, EXPLAINs for queries above explain_threshold, and
      a final count of queries after every HTTP request
      """
      explain_threshold = 0.5  # EXPLAIN queries that ran for more than 0.5s
      queries = get_debug_queries()
      # We have to copy the queries list below otherwise queries executed
      # in the for loop will be appended causing an endless loop
      for query in queries[:]:
        app.logger.info("{:.8f} {}\n{}".format(
            query.duration,
            query.context,
            query.statement % query.parameters))
        if query.duration > explain_threshold:
          statement = 'EXPLAIN ' + query.statement
          engine = SQLAlchemy().get_engine(app)
          result = engine.execute(statement, query.parameters)
          app.logger.info(tabulate(result.fetchall(), headers=result.keys()))
      app.logger.info("Total queries: {}".format(len(queries)))
      return response


_enable_debug_toolbar()
_enable_jasmine()
_display_sql_queries()
