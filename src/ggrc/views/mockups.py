# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc.app import app
from ggrc.login import login_required
from flask import render_template
from ggrc import settings


def init_mockup_views():

  # Do not load mockup views in production
  if settings.PRODUCTION:
    return

  @app.route("/mockups/sample")
  @login_required
  def mockup_sample():
    return render_template("mockups/sample.haml")

  @app.route("/mockups/new_mockup")
  @login_required
  def mockup_sample2():
    return render_template("mockups/base.haml")
