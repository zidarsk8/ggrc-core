# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


from ggrc.app import app
from ggrc.extensions import get_extension_modules
from ggrc.login import login_required
from ggrc import settings
from flask import current_app, request, session, redirect

GOOGLE_CLIENT_ID= getattr(settings, 'GAPI_CLIENT_ID')
GOOGLE_SECRET_KEY= getattr(settings, 'SECRET_KEY')

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

@app.route("/calendar_oauth_request", methods=["GET", "POST"])
@login_required
def handle_calendar_oauth():
  from oauth2client.client import OAuth2WebServerFlow
  flow = OAuth2WebServerFlow(client_id=GOOGLE_CLIENT_ID, 
    client_secret=GOOGLE_SECRET_KEY,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=request.url_root + 'oauth2callback/calendar') 
  auth_uri=flow.step1_get_authorize_url()
  current_app.logger.info("auth uri: " + auth_uri + " redirect uri: " + request.url_root + \
        "oauth2callback/calendar") 
  return redirect(auth_uri)

@app.route("/oauth2callback/calendar", methods=["GET", "POST"])
def handle_calendar_flow_auth():
  error_return=request.args.get("error")
  code=request.args.get("code")
  if error_return is not None:
    current_app.logger.error("Error occured in Calendar flow authorization: " + error_return)
    return 'Error'
  session['oauth_code']=code
  current_app.logger.info("oauth_credentials is set")
  return 'Ok'

@app.route("/notify_email_deferred", methods=["GET", "POST"])
def notify_email_deferred():
  for extension_module in get_extension_modules():
    if hasattr(extension_module, 'notify_email_deferred'):
      extension_module.notify_email_deferred()
  return 'Ok'
