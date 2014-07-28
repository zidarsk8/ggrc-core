# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: silas@reciprocitylabs.com
# Maintained By: silas@reciprocitylabs.com

from ggrc.app import app
from ggrc.login import login_required

from flask import render_template


@app.route("/risk_admin")
@login_required
def risk_admin():
  """Special admin page to show risks
  TODO: Dry this up, override existing admin url.
  """
  return render_template("admin/risk_index.haml")
