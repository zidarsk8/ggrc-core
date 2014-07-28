# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com

from ggrc.app import app
from ggrc.login import login_required
from ggrc_risk_assessment_v2.views import converters

from flask import render_template


def risk_admin():
  """Special admin page to show risks
  TODO: Dry this up, override existing admin url.
  """
  return render_template("admin/risk_index.haml")


def init_extra_views(app):
  app.add_url_rule(
      "/risk_admin", "risk_admin",
      view_func=login_required(risk_admin))
  converters.init_extra_views(app)
