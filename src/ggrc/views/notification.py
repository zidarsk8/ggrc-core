# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from flask import current_app, request, redirect
from ggrc.app import app
from ggrc import db
from ggrc.login import login_required
from ggrc.models import all_models
from ggrc.notification import EmailNotification, EmailDigestNotification, CalendarService
from ggrc_workflows.notification import *
from datetime import datetime
from oauth2client.client import OAuth2WebServerFlow
from ggrc import settings

TEST_CYCLE_ID=1

WORKFLOW_CYCLE_DUE=3
WORKFLOW_CYCLE_STARTING=7

"""
@app.route("/modify_status", methods=["GET", "POST"])
@login_required
def modify_status():
  model=request.args.get('model')
  id=request.args.get('id')
  status=request.args.get('status')
  cls=getattr(all_models, model)
  obj=cls.query.filter(cls.id == int(id)).first()
  if obj is not None:
    obj.status=status
    db.session.add(obj)
    db.session.commit()
    src_obj={'status': status}
    if model in ['CycleTaskGroupObjectTask']:
      handle_task_put(sender=None, obj=obj, src=src_obj, service=None)
    db.session.commit()
  return 'Ok'

@app.route("/prepare_email", methods=["GET", "POST"])
@login_required
def prepare_email_ggrc_users():
  model=request.args.get('model')
  id=request.args.get('id')
  cls=getattr(all_models, model)
  obj=cls.query.filter(cls.id == int(id)).first()
  if obj is not None:
    target_objs=[]
    recipients=[obj.contact]
    email_notification=EmailNotification()
    if obj is not None:
      subject=obj.type + " " + obj.title + " created"
      content=obj.type + ": " + obj.title + " : " + request.url_root + obj._inflector.table_plural + \
       "/" + str(obj.id) + " created on " + str(obj.created_at)
      email_notification.prepare(target_objs, obj.contact, recipients, subject, content)
      db.session.commit()
  return 'Ok'

@app.route("/prepare_emaildigest", methods=["GET", "POST"])
@login_required
def prepare_email_digest_ggrc_users():
  model=request.args.get('model')
  id=request.args.get('id')
  import ggrc.models
  cls=getattr(all_models, model)
  obj=cls.query.filter(cls.id == int(id)).first()
  if obj is not None:
    target_objs=[]
    recipients=[obj.contact]
    email_digest_notification = EmailDigestNotification()
    if obj is not None:
      subject=obj.type + " " + "Email Digest for " + datetime.now().strftime('%Y/%m/%d')
      content=obj.type + ": " + obj.title + " : " + request.url_root + obj._inflector.table_plural+ \
       "/" + str(obj.id) + " created on " + str(obj.created_at)
      email_digest_notification.prepare(target_objs, obj.contact, recipients, subject, content)
      db.session.commit()
  return 'Ok'

@app.route("/notify_email", methods=["GET", "POST"])
@login_required
def notify_email_ggrc_users():
  email_notification=EmailNotification()
  email_notification.notify()
  db.session.commit()
  return 'Ok'
"""
# AppEngine cron supports only GET
# ToDo(Mouli): Cron job to check all model extensions and invoke notify_email_digest
# Each model extension has a trigger to handle respective models such as ggrc_workflows
#
@app.route("/notify_emaildigest", methods=["GET", "POST"])
def notify_email_digest_ggrc_users():
  """ handle any outstanding tasks and newly starting workflow cycles prior to notify email digest
  """
  handle_tasks_overdue()
  handle_workflow_cycle_overdue()
  handle_workflow_cycle_due(WORKFLOW_CYCLE_DUE)
  handle_workflow_cycle_started()
  handle_workflow_cycle_starting(WORKFLOW_CYCLE_STARTING)
  db.session.commit()

  """ notify email digest 
  """
  email_digest_notification=EmailDigestNotification()
  email_digest_notification.notify()
  db.session.commit()
  return 'Ok'

GOOGLE_CLIENT_ID= getattr(settings, 'GAPI_CLIENT_ID')
GOOGLE_SECRET_KEY= getattr(settings, 'SECRET_KEY')

@app.route("/workflow_calendar", methods=["GET", "POST"])
def handle_workflow_calendar_event():
  flow = OAuth2WebServerFlow(client_id=GOOGLE_CLIENT_ID, 
    client_secret=GOOGLE_SECRET_KEY,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=request.url_root + 'oauth2callback')
  auth_uri=flow.step1_get_authorize_url()
  current_app.logger.info("auth uri: " + auth_uri + " redirect uri: " + request.url_root + "oauth2callback")
  return redirect(auth_uri)

@app.route("/oauth2callback", methods=["GET", "POST"])
def handle_calendar_flow_auth():
  error_return=request.args.get("error")
  code=request.args.get("code")
  if error_return is not None:
    current_app.logger.error("Error occured in Calendar flow authorization: " + error_return)
    return 'Error'
  cycle=get_cycle_by_id(TEST_CYCLE_ID)
  if cycle is None:
    current_app.logger.error("Error occured in getting cycle object: ")
    return 'Error'
  flow = OAuth2WebServerFlow(client_id=GOOGLE_CLIENT_ID, 
    client_secret=GOOGLE_SECRET_KEY,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=request.url_root + 'oauth2callback')
  credentials=flow.step2_exchange(code)
  calendar_service=CalendarService(credentials)
  calendar_service.handle_workflow_start(cycle)
  db.session.commit()
  return 'Ok'
