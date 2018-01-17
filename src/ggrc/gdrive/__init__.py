# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""GDrive module"""

import httplib2

import flask

from ggrc import settings
from ggrc.app import app

from oauth2client import client

_GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
_GOOGLE_TOKEN_URI = "https://accounts.google.com/o/oauth2/token"
_GOOGLE_API_GDRIVE_SCOPE = "https://www.googleapis.com/auth/drive"


def get_http_auth():
  """Get valid user credentials from storage and create an authorized
  http from it.

  If nothing has been stored, or if the stored credentials are invalid,
  the OAuth2 flow is completed to obtain the new credentials.

  Returns:
      http instance authorized with the credentials
  """
  credentials = client.OAuth2Credentials.from_json(
      flask.session['credentials'])
  http_auth = credentials.authorize(httplib2.Http())
  if credentials.access_token_expired:
    credentials.refresh(http_auth)
    flask.session['credentials'] = credentials.to_json()
  return http_auth


def verify_credentials():
  """Verify credentials to gdrive for the current user

  :return: None, if valid credentials are present, or redirect to authorize fn
  """
  if 'credentials' not in flask.session:
    return authorize_app()
  credentials = client.OAuth2Credentials.from_json(
      flask.session['credentials'])
  if credentials.access_token_expired:
    return authorize_app()
  return None


@app.route("/authorize")
def authorize_app():
  """Redirect to Google API auth page to authorize"""
  flow = client.OAuth2WebServerFlow(
      settings.GAPI_CLIENT_ID,
      settings.GAPI_CLIENT_SECRET,
      scope=_GOOGLE_API_GDRIVE_SCOPE,
      redirect_uri=flask.url_for("authorize_app", _external=True),
      auth_uri=_GOOGLE_AUTH_URI,
      token_uri=_GOOGLE_TOKEN_URI,
  )
  if 'code' not in flask.request.args:
    # `state` is where we want to redirect once the auth is done
    auth_uri = flow.step1_get_authorize_url(state=flask.request.url)
    return flask.redirect(auth_uri)

  auth_code = flask.request.args["code"]
  credentials = flow.step2_exchange(auth_code)
  flask.session['credentials'] = credentials.to_json()
  return flask.redirect(flask.request.args['state'])
