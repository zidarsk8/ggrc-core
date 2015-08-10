# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from ggrc.app import app
from ggrc.login import login_required
from flask import render_template


def init_mockup_views():

  @app.route("/mockups/v1.0/program.html")
  @login_required
  def mockup():
    """The mockup program guide page
    """
    return render_template("mockups/v1.0/program.html")

  @app.route("/mockups/v1.0/assessment.html")
  @login_required
  def assessments():
    """The assessments guide page
    """
    return render_template("mockups/v1.0/assessment.html")

  @app.route("/mockups/v1.0/assessment-start.html")
  @login_required
  def assessments_start():
    """The assessment start guide page
    """
    return render_template("mockups/v1.0/assessment-start.html")

  @app.route("/mockups/v1.0/object.html")
  @login_required
  def assessments_object():
    """The assessment object guide page
    """
    return render_template("mockups/v1.0/object.html")

  @app.route("/mockups/v1.0/object-final.html")
  @login_required
  def assessments_object_final():
    """The assessment object final guide page
    """
    return render_template("mockups/v1.0/object-final.html")

  @app.route("/mockups/v1.0/my-work.html")
  @login_required
  def assessments_my_work():
    """The assessment my work guide page
    """
    return render_template("mockups/v1.0/my-work.html")

  @app.route("/mockups/assessments_grid")
  @login_required
  def assessments_grid():
    """The assessments grid guide page
    """
    return render_template("mockups/assessments-grid.html")

  @app.route("/mockups/v1.1/index.html")
  @login_required
  def workflow_assessment():
    """The workflow assessment guide page
    """
    return render_template("mockups/v1.1/index.html")

  @app.route("/mockups/v1.1/workflow.html")
  @login_required
  def workflow_info():
    """The workflow info guide page
    """
    return render_template("mockups/v1.1/workflow.html")

  @app.route("/mockups/rapid-data-entry/index.html")
  @login_required
  def rapid_data_entry():
    """Rapid data entry mockup
    """
    return render_template("mockups/rapid-data-entry/index.html")

  @app.route("/mockups/custom-attributes/index.html")
  @login_required
  def custom_attributes():
    """Custom attributes mockup
    """
    return render_template("mockups/custom-attributes/index.html")

  @app.route("/mockups/data-grid/")
  @login_required
  def reporting():
    """Reporting mockup
    """
    return render_template("mockups/data-grid/index.html")

  @app.route("/mockups/dashboard-ui/index.html")
  @login_required
  def dashboard_ui():
    """Dashboard UI UX mockup
    """
    return render_template("mockups/dashboard-ui/index.html")

  @app.route("/mockups/dashboard-ui/object.html")
  @login_required
  def object_ui():
    """Object UI UX mockup
    """
    return render_template("mockups/dashboard-ui/object.html")

  @app.route("/mockups/dashboard-ui/tree.html")
  @login_required
  def tree_ui():
    """Tree UI UX mockup
    """
    return render_template("/mockups/dashboard-ui/tree.html")

  @app.route("/mockups/dashboard-ui/workflow.html")
  @login_required
  def workflow_ui():
    """Workflow UI UX mockup
    """
    return render_template("/mockups/dashboard-ui/workflow.html")

  @app.route("/mockups/dashboard-ui/workflow-info.html")
  @login_required
  def workflow_info_ui():
    """Workflow info UI UX mockup
    """
    return render_template("/mockups/dashboard-ui/workflow-info.html")

  @app.route("/mockups/dashboard-ui/workflow-people.html")
  @login_required
  def workflow_people_ui():
    """Workflow people UI UX mockup
    """
    return render_template("/mockups/dashboard-ui/workflow-people.html")

  @app.route("/mockups/dashboard-ui/audit.html")
  @login_required
  def audit_ui():
    """Audit UI UX mockup
    """
    return render_template("/mockups/dashboard-ui/audit.html")

  @app.route("/mockups/dashboard-ui/audit-info.html")
  @login_required
  def audit_info_ui():
    """Audit info UI UX mockup
    """
    return render_template("/mockups/dashboard-ui/audit-info.html")

  @app.route("/mockups/dashboard-ui/audit-people.html")
  @login_required
  def audit_people_ui():
    """Audit people UI UX mockup
    """
    return render_template("/mockups/dashboard-ui/audit-people.html")

  @app.route("/mockups/audit-revamp/info.html")
  @login_required
  def audit_info_revamp():
    """Audit info revamp mockup
    """
    return render_template("/mockups/audit-revamp/info.html")

  @app.route("/mockups/audit-revamp/issues.html")
  @login_required
  def audit_info_issues_revamp():
    """Audit info issues revamp mockup
    """
    return render_template("/mockups/audit-revamp/issues.html")

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

  @app.route("/mockups/data-grid/export-object.html")
  @login_required
  def data_grid_export_object():
    """Data grid export object mockup
    """
    return render_template("mockups/data-grid/export-object.html")

  @app.route("/mockups/risk-assessment")
  @login_required
  def risk_assessment_redesign():
    """Risk Assessment mockup
    """
    return render_template("/mockups/risk-assessment/index.html")
