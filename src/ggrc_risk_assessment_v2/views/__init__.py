# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: dan@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

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
