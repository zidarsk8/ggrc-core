# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


from ggrc.app import app
from ggrc.extensions import get_extension_modules
from ggrc.login import login_required

"""
This contains the endpoint for gGRC notifications and can be invoked from UI or Cron 
AppEngine Cron job invokes REST GET API and hence GET is specified in notify_emaildigest

"""
@app.route("/notify_emaildigest", methods=["GET", "POST"])
def notify_emaildigest():
  for extension_module in get_extension_modules():
    if hasattr(extension_module, 'notify_email_digest'):
      extension_module.notify_email_digest()
  return 'Ok'

@app.route("/calendar/<resource>/<id>", methods=["GET", "POST"])
@login_required
def handle_calendar_request(resource, id):
  for extension_module in get_extension_modules():
    if hasattr(extension_module, 'handle_calendar_request'):
      return extension_module.handle_calendar_request(resource, id)
  return 'Ok'
  
@app.route("/oauth2callback/calendar", methods=["GET", "POST"])
def handle_calendar_flow_auth():
  for extension_module in get_extension_modules():
    if hasattr(extension_module, 'handle_calendar_flow_auth'):
      return extension_module.handle_calendar_flow_auth()
  return 'Ok'

@app.route("/notify_email_deferred", methods=["GET", "POST"])
def notify_email_deferred():
  for extension_module in get_extension_modules():
    if hasattr(extension_module, 'notify_email_deferred'):
      extension_module.notify_email_deferred()
  return 'Ok'
