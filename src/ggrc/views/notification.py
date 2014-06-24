# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from flask import current_app, request, render_template
from ggrc.app import app
from ggrc import db
from ggrc.login import login_required
from ggrc.models import all_models
from ggrc.notification import EmailNotification, EmailDigestNotification
from ggrc_workflows.notification import *
from datetime import datetime
import flask
from flask.ext.login import current_user

@app.route("/modify_status", methods=["GET", "POST"])
@login_required
def modify_status():
  """ prepare email digest
  """
  model = request.args.get('model')
  id = request.args.get('id')
  status = request.args.get('status')
  cls = getattr(all_models, model)
  obj = cls.query.filter(cls.id == int(id)).first()
  if obj is not None:
    obj.status=status
    db.session.add(obj)
    db.session.commit()
    if model in ['CycleTaskGroupObjectTask']:
      handle_task_put(sender=None, obj=obj, src=obj, service=None)
    db.session.commit()
  return 'Ok'

@app.route("/prepare_email", methods=["GET", "POST"])
@login_required
def prepare_email_ggrc_users():
  """ prepare email digest
  """
  model = request.args.get('model')
  id = request.args.get('id')
  cls = getattr(all_models, model)
  obj = cls.query.filter(cls.id == int(id)).first()
  if obj is not None:
    target_objs=[]
    recipients=[obj.contact]
    email_notification = EmailNotification()
    if obj is not None:
      subject = obj.type + " " + obj.title + " created"
      content = obj.type + ": " + obj.title + " : " + request.url_root + obj._inflector.table_plural + \
       "/" + str(obj.id) + " created on " + str(obj.created_at)
      email_notification.prepare(target_objs, obj.contact, recipients, subject, content)
      db.session.commit()
  return 'Ok'


@app.route("/prepare_emaildigest", methods=["GET", "POST"])
@login_required
def prepare_email_digest_ggrc_users():
  """ prepare email digest
  """
  model = request.args.get('model')
  id = request.args.get('id')
  import ggrc.models
  cls = getattr(all_models, model)
  obj = cls.query.filter(cls.id == int(id)).first()
  if obj is not None:
    target_objs=[]
    recipients=[obj.contact]
    email_digest_notification = EmailDigestNotification()
    if obj is not None:
      subject = obj.type + " " + "Email Digest for " + datetime.now().strftime('%Y/%m/%d')
      content = obj.type + ": " + obj.title + " : " + request.url_root + obj._inflector.table_plural+ \
       "/" + str(obj.id) + " created on " + str(obj.created_at)
      email_digest_notification.prepare(target_objs, obj.contact, recipients, subject, content)
      db.session.commit()
  return 'Ok'


@app.route("/notify_email", methods=["GET", "POST"])
@login_required
def notify_email_ggrc_users():
  """ notify email for a program object
  """
  email_notification = EmailNotification()
  email_notification.notify()
  db.session.commit()
  return 'Ok'


@app.route("/notify_emaildigest", methods=["GET", "POST"])
def notify_email_digest_ggrc_users():
  """ handle any outstading tasks prior to notify email digest
  """
  current_app.logger.info("notify email digest invoked")
  handle_tasks_overdue()
  handle_tasks_due(2)
  handle_workflow_cycle_status_change('Completed')
  handle_workflow_cycle_started()
  handle_workflow_cycle_starting(7)
  db.session.commit()

  """ notify email digest 
  """
  email_digest_notification = EmailDigestNotification()
  email_digest_notification.notify()
  db.session.commit()
  return 'Ok'


@app.route("/api/set_active_notifications",
           methods=["POST"])
@login_required
def set_active_notifications():
  """
  Sets notification config for user
  """
  if not current_user:
    return flask.jsonify({'result': False})

  active = request.json.get('active', [])
  notificationConfig = all_models.NotificationConfig.query.\
      filter(all_models.NotificationConfig.person_id == current_user.id).all()

  if(len(notificationConfig) == 0):
    types = all_models.NotificationConfig.VALID_TYPES
    for type in types:
      notificationConfig.append(all_models.NotificationConfig(
                                person_id=current_user.id,
                                notif_type=type,
                                enable_flag=False)
                                )
  for nc in notificationConfig:
    nc.enable_flag = nc.notif_type in active
    db.session.add(nc)

  db.session.commit()
  return flask.jsonify({'result': True})
