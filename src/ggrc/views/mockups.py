# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

# Disable pylint warnings for unsued variables that are caused by the decorated
# functions: mockup_home, mockup_request, mockup_assessor, mockup_workflow,
# mockup_quick_workflow
# pylint: disable=W0612

"""Basic mockup views."""

from flask import render_template
from ggrc.app import app
from ggrc.login import login_required
from ggrc import settings


def init_mockup_views():
  """Init function for all mockup views."""

  # Do not load mockup views in production
  if settings.PRODUCTION:
    return

  @app.route("/mockups")
  @login_required
  def mockup_home():
    return render_template("mockups/home.haml")

  @app.route("/mockups/request")
  @login_required
  def mockup_request():
    return render_template("mockups/request.haml")

  @app.route("/mockups/assessor")
  @login_required
  def mockup_assessor():
    return render_template("mockups/assessor.haml")

  @app.route("/mockups/workflow")
  @login_required
  def mockup_workflow():
    return render_template("mockups/workflow.haml")

  @app.route("/mockups/quick-workflow")
  @login_required
  def mockup_quick_workflow():
    return render_template("mockups/quick-workflow.haml")
