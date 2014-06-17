# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


from flask import current_app, request
import ggrc_workflows.models as models
from ggrc.notification import EmailNotification, EmailDigestNotification
from datetime import datetime, timedelta
from ggrc.services.common import Resource
from ggrc.models import Person
from ggrc import db

PRI_TASK_OVERDUE=1
PRI_TASK_DUE=2
PRI_TASK_ASSIGNMENT=3
PRI_TASK_CHANGES=4
PRI_OTHERS=5

def get_workflow_for_task(task_id):
  workflow_task = db.session.query(models.WorkflowTask).\
    join(models.WorkflowTask.task).\
    filter(models.Task.id == task_id).first()
  if workflow_task is not None:
    return db.session.query(models.Workflow).filter(models.Workflow.id == workflow_task.workflow_id).first()
  else:
   return None

def get_cycle_for_task(taskgroup_object_id):
  taskgroup= db.session.query(models.CycleTaskGroup).\
    join(models.CycleTaskGroupObject).\
    filter(models.TaskGroupObject.id == taskgroup_object_id).first()
  if taskgroup is not None:
    return db.session.query(models.Cycle).filter(models.Cycle.id == taskgroup.cycle_id).first()
  else:
   return None

def handle_tasks_overdue():
  tasks = db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date > datetime.today()).all()
  for task in tasks:
    subject=task.type + '"' + task.title + '" ' + " is past overdue " 
    content=task.type + ": " + task.title + " : " + request.url_root + task._inflector.table_plural + \
      "/" + str(task.id) + " due on " + str(task.end_date)
    notif_type = 'Email_Digest'
    contact = db.session.query(Person).filter(Person.id == task.contact_id).first()
    if contact is None:
      current_app.logger.info("Trigger: Contact attribute is not set")
      continue 
    recipients = [contact]
    notif_pri = PRI_TASK_OVERDUE
    prepare_notification(task, notif_type, notif_pri, subject, content, task.owner, recipients)
  db.session.commit()

def handle_task_due(num_days):
  tasks = db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date > datetime.today()-timedelta(num_days)).all()
  for task in tasks:
    subject=task.type + '"' + task.title + '" ' + " is due in " + str(days) + " num_days"
    content=task.type + ": " + task.title + " : " + request.url_root + task._inflector.table_plural + \
      "/" + str(task.id) + " due on " + str(task.end_date)
    notif_type = 'Email_Digest'
    contact = db.session.query(Person).filter(Person.id == task.contact_id).first()
    if contact is None:
      current_app.logger.info("Trigger: Contact attribute is not set")
      continue 
    recipients = [contact]
    notif_pri = PRI_TASKS_DUE
    prepare_notification(task, notif_type, notif_pri, subject, content, task.contact, recipients)
  db.session.commit()

def handle_workflow_cycle_status_change(status):
  workflow_cycles= db.session.query(models.Cycle).all()
  for cycle in workflow_cycles:
    workflow_obj=db.session.filter(models.Workflow.id == cycle.workflow_id).first()
    for task in workflow_obj.tasks:
      if task.status != status:
        continue
      subject=workflow.type + '"' + workflow.title + '" ' + " is ready to be " + status   
      content=task.type + ": " + task.title + " : " + request.url_root + task._inflector.table_plural + \
        "/" + str(task.id) + " due on " + str(task.end_date)
      notif_type = 'Email_Digest'
      recipients = [task.owner]
      prepare_notification(task, notif_type, notif_pri, subject, content, cycle.owner, recipients)
  db.session.commit()

def handle_workflow_cycle_started(num_days):
  workflow_cycles= db.session.query(models.Cycle).all()
  for cycle in workflow_cycles:
    if cycle.status != 'Started' and (cycle.end_date - datetime.today()) == timedelta(num_days):
      subject=cycle.type + '"' + cycle.title + '" ' + " will start in " + str(num_days) + " days"
      content=cycle.type + ": " + cycle.title + " : " + request.url_root + task._inflector.table_plural + \
          "/" + str(task.id) + " due on " + str(task.end_date)
      notif_type = 'Email_Digest'
      notif_pri = PRI_OTHERS
      workflow_obj=db.session.filter(models.Workflow.id == cycle.workflow_id).first()
      if workflow_obj is None:   
        continue
      recipients=[]
      for task in workflow_obj.tasks:
        recipients.append(task.owner)
      if len(recipients):
        prepare_notification(task, notif_type, notif_pri, subject, content, cycle.owner, recipients)
  db.session.commit()

#ToDo(Mouli) uncomment the trigger after edit modal is completed
#@Resource.model_put.connect_via(models.CycleTaskGroupObjectTask)
def handle_task_put(sender, obj=None, src=None, service=None):
  current_app.logger.info("Trigger: Task PUT: " + "status: " + src.status + "obj: " + str(obj))
  if not getattr(obj, 'status'): 
    current_app.logger.info("Trigger: Status attribute is not modified")
    return
  current_app.logger.info("Status is changed to  " + obj.status)
  notif_pri=PRI_TASK_CHANGES
  contact = db.session.query(Person).filter(Person.id == src.contact_id).first()
  if contact is None:
    current_app.logger.info("Trigger: Task Contact attribute is not set")
    return
  subject=src.type + '"' + src.title + '" ' + " has been " + src.status +  " by " + contact.name
  content=src.type + ": " + src.title + " : " + request.url_root + src._inflector.table_plural + \
    "/" + str(obj.id) + " due on " + str(src.end_date)
  if obj.status in ['InProgress', 'Declined', 'Verified']: 
    notif_type='Email_Now'
    cycle_obj = get_cycle_for_task(src.cycle_task_group_object_id)
    if cycle_obj is None:
      current_app.logger.error("Unable to find workflow cycle for task: " + src.title)
    cycle_contact = db.session.query(Person).filter(Person.id == cycle_obj.contact_id).first()
    if cycle_contact is None:
      current_app.logger.info("Trigger: Cycle Contact attribute is not set")
      return
    recipients = [cycle_contact]
    prepare_notification(src, notif_type, notif_pri, subject, content, contact, recipients)
    if obj.status in ['Verified']: 
      notif_type='Email_Digest'
      prepare_notification(src, notif_type, notif_pri, subject, content, contact, recipients)
  if obj.status in ['Completed']: 
    recipients=[cycle_obj.contact]
    notif_type='Email_Digest'
    workflow_obj = get_workflow_for_task(src.task_group_task_id) 
    if workflow_obj is None:
      current_app.logger.error("Unable to find workflow for task: " + src.title)
      return
    recipients = [workflow_obj.contact]
    prepare_notification(src, notif_type, notif_pri, subject, content, src.contact, recipients)

def prepare_notification(src, notif_type, notif_pri, subject, content, owner, recipients, override=False):
  if notif_type == 'Email_Digest':
    emaildigest_notification = EmailDigestNotification()
    emaildigest_notification.notif_pri = notif_pri
    emaildigest_notification.prepare([src], owner, recipients, subject, content)
  elif notif_type == 'Email_Now':
    email_notification = EmailNotification()
    email_notification.notif_pri = notif_pri
    notification = email_notification.prepare([src], owner, recipients, subject, content)
    email_notification.notify_one(notification)
  else:
    return None
  if override is True and notif_type != 'Email_Now':
    email_notification = EmailNotification()
    email_notification.notif_pri = notif_pri
    notification = email_notification.prepare([src], owner, recipients, subject, content)
    email_notification.notify_one(notification)
