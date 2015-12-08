# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc.app import app
from ggrc.login import login_required
from ggrc_risks.views import converters

from flask import render_template


def risk_admin():
  """Special admin page to show risks
  TODO: Dry this up, override existing admin url.
  """
  return render_template("admin/risk_index.haml")


def init_extra_views(app):
  pass
