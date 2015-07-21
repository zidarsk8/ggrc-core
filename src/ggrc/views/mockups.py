# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc.app import app
from ggrc.login import login_required
from flask import render_template


def init_mockup_views():

  @app.route("/mockups/audit-3.0/")
  @login_required
  def audit_3_0():
    """Audit 3.0 mockup
    """
    return render_template("/mockups/audit-3.0/info.html")

  @app.route("/mockups/audit-3.0/control-assessment.html")
  @login_required
  def audit_3_0_ca():
    """Audit 3.0 CA mockup
    """
    return render_template("/mockups/audit-3.0/control-assessment.html")

  @app.route("/mockups/import/")
  @login_required
  def import_redesign():
    """Import prototype
    """
    return render_template("/mockups/import/index.html")

  @app.route("/mockups/export/")
  @login_required
  def export_redesign():
    """Export prototype
    """
    return render_template("/mockups/export/index.html")

  @app.route("/mockups/export-object/")
  @login_required
  def export_object_redesign():
    """Export object prototype
    """
    return render_template("/mockups/export/object.html")

  @app.route("/mockups/risk-assessment")
  @login_required
  def risk_assessment_redesign():
    """Risk Assessment mockup
    """
    return render_template("/mockups/risk-assessment/index.html")
