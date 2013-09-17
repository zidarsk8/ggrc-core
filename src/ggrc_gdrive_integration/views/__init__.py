from ggrc.app import app
from ggrc.login import login_required
from flask import render_template
from ggrc.views import base_context

@app.context_processor
def gdrive_context():
  ctx = base_context()
  def instance_json():
    return "null"
  ctx["instance_json"] = instance_json
  return ctx

@app.route("/gdrive_sandbox")
@login_required
def sandbox():
  """A demo page for GDrive integration models
  """
  return render_template("sandbox/index.haml")
