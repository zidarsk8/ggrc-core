# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


from flask import current_app, request
import ggrc_workflows.models as models
from ggrc.notification import EmailNotification, EmailDigestNotification
from datetime import date, timedelta
from ggrc.services.common import Resource
from ggrc.models import Person
from ggrc import db

PRI_TASK_OVERDUE=1
PRI_TASK_DUE=2
PRI_TASK_ASSIGNMENT=3
PRI_TASK_CHANGES=4
PRI_OTHERS=5

def get_workflow_owner(task):
  cycle = get_cycle(task) 
  if cycle is None:
    current_app.logger.warn("Trigger: cycle object is not found")
    return None
  if cycle.contact_id is not None:
    return db.session.query(Person).filter(Person.id==cycle.contact_id).first()
  else:
    return None

def get_assignee(task):
  if task.contact_id is not None:
    return db.session.query(Person).filter(Person.id==task.contact_id).first()
  task_group = get_taskgroup(task)
  if task_group is not None and task_group.contact_id is not None:
    return db.session.query(Person).filter(Person.id==task_group.contact_id).first()
  if task_group is None:
    current_app.logger.warn("Trigger: CycleTaskGroup object is not found")
    return None
  cycle = get_taskgroup_cycle(task_group)
  if cycle is not None and cycle.contact_id is not None:
    return db.session.query(Person).filter(Person.id==cycle.contact_id).first()
  if cycle is None:
    current_app.logger.warn("Trigger: Cycle object is not found")
    return None

def get_workflow(task):
  cycle = get_cycle(task)
  if cycle is None:
    current_app.logger.warn("Trigger: Cycle object is not found")
    return None
  return db.session.query(models.Workflow).\
    filter(models.Workflow.id == cycle.workflow_id).first()
   
def get_cycle(task):
  task_group = get_taskgroup(task) 
  if task_group is None:
    current_app.logger.warn("Trigger: CycleTaskGroup object is not found")
    return None
  return db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.id == task_group.cycle_id).first()

def get_taskgroup_cycle(task_group):
  return db.session.query(models.Cycle).\
    filter(models.Cycle.id == task_group.cycle_id).first()

def get_cycle_workflow(cycle):
  workflow = db.session.query(models.Workflow).\
    filter(models.Workflow.id == cycle.workflow_id).first()
  return workflow

def get_taskgroup_object(task):
  task_group_object= db.session.query(models.CycleTaskGroupObject).\
    filter(models.CycleTaskGroupObject.id == task.cycle_task_group_object_id).first()
  return task_group_object

def get_taskgroup(task):
  task_group_object = get_taskgroup_object(task)
  if task_group_object == None:
    return None
  task_group = db.session.query(models.CycleTaskGroup).\
    filter(models.CycleTaskGroup.id == task_group_object.cycle_task_group_id).first()
  return task_group

def handle_tasks_overdue():
  tasks = db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date < date.today()).\
    filter(models.CycleTaskGroupObjectTask.status != 'Completed').\
    filter(models.CycleTaskGroupObjectTask.status != 'Verified').\
    all()
  for task in tasks:
    subject="Task " + '"' + task.title + '" ' + "is past overdue " 
    content=subject + " URL: " + request.url_root + \
      models.Task.__tablename__ + "/" + str(task.task_group_task_id)
    notif_type = 'Email_Digest'
    workflow_owner = get_workflow_owner(task)
    if workflow_owner is None:
      current_app.logger.warn("Unable to find workflow owner for task: " + task.title)
      return
    assignee = get_assignee(task)
    if assignee is None:
      current_app.logger.warn("Unable to find assignee for task: " + task.title)
      return
    recipients = [assignee]
    notif_pri = PRI_TASK_OVERDUE
    prepare_notification(task, notif_type, notif_pri, subject, content, workflow_owner, recipients)

def handle_tasks_due(num_days):
  tasks = db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date == (date.today() + timedelta(num_days))).\
    filter(models.CycleTaskGroupObjectTask.status != 'Completed').\
    filter(models.CycleTaskGroupObjectTask.status != 'Verified').\
    all()
  for task in tasks:
    subject="Task " + '"' + task.title + '" ' + "is due in " + str(num_days) + " days"
    content=subject + " URL: " + request.url_root + models.Task.__tablename__ + \
      "/" + str(task.task_group_task_id) 
    notif_type = 'Email_Digest'
    workflow_owner = get_workflow_owner(task)
    if workflow_owner is None:
      current_app.logger.warn("Unable to find workflow owner for task: " + task.title)
      return
    assignee = get_assignee(task)
    if assignee is None:
      current_app.logger.warn("Unable to find assignee for task: " + task.title)
      return
    recipients = [assignee]
    notif_pri = PRI_TASK_DUE
    prepare_notification(task, notif_type, notif_pri, subject, content, workflow_owner, recipients)

def handle_workflow_cycle_status_change(status):
  if status not in ['Completed', 'Verified']:
    return
  workflow_cycles= db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.status == status).all()
  for cycle in workflow_cycles:
    workflow_obj=db.session.query(models.Workflow).\
      filter(models.Workflow.id == cycle.workflow_id).first()
    if workflow_obj is None:
      current_app.logger.warn("Trigger: Unable to find workflow")
      continue
    if status == 'Verified':
       new_status = 'Finished'
    else:
       new_status = 'Verified'
    recipients=[]
    for person in workflow_obj.people:
      recipients.append(person)
    if len(recipients):
      subject="Workflow Cycle " + '"' + cycle.title + '" ' + "is ready to be "  + new_status
      content=subject + " URL: " + request.url_root + workflow_obj._inflector.table_plural + \
        "/" + str(workflow_obj.id) + "#current_widget" 
      notif_type = 'Email_Digest'
      notif_pri = PRI_OTHERS
      prepare_notification(cycle, notif_type, notif_pri, subject, content, \
        cycle.contact, recipients)

def handle_workflow_cycle_started():
  workflow_cycles= db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.status == 'InProgress').\
    filter(models.Cycle.start_date == date.today()).\
    all()
  for cycle in workflow_cycles:
    workflow_obj=db.session.query(models.Workflow).\
      filter(models.Workflow.id == cycle.workflow_id).first()
    if workflow_obj is None:
      current_app.logger.warn("Trigger: Unable to find workflow")
      continue
    subject="Workflow Cycle " + '"' + cycle.title + '" ' + "started " + str(cycle.start_date) 
    content=subject + " URL: " + request.url_root + workflow_obj._inflector.table_plural + \
      "/" + str(workflow_obj.id) + "#current_widget"
    notif_type = 'Email_Digest'
    notif_pri = PRI_OTHERS
    recipients=[]
    for person in workflow_obj.people:
      recipients.append(person)
    if len(recipients):
      prepare_notification(cycle, notif_type, notif_pri, subject, content, \
       cycle.contact, recipients)

def handle_workflow_cycle_starting(num_days):
  workflow_cycles= db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.start_date == (date.today() + timedelta(num_days))).\
    all()
  for cycle in workflow_cycles:
    workflow_obj=db.session.query(models.Workflow).\
      filter(models.Workflow.id == cycle.workflow_id).first()
    if workflow_obj is None:
      current_app.logger.warn("Trigger: Unable to find workflow")
      continue
    subject="Workflow Cycle " + '"' + cycle.title + '" ' + "will start in " + str(num_days) + " days"
    content=subject + " URL: " + request.url_root + workflow_obj._inflector.table_plural + \
      "/" + str(workflow_obj.id) + "#current_widget" 
    notif_type = 'Email_Digest'
    notif_pri = PRI_OTHERS
    recipients=[]
    for person in workflow_obj.people:
      recipients.append(person)
    if len(recipients):
      prepare_notification(cycle, notif_type, notif_pri, subject, content, \
        cycle.contact, recipients)

#@Resource.model_put.connect_via(models.CycleTaskGroupObjectTask)
def handle_task_put(sender, obj=None, src=None, service=None):
  if not getattr(obj, 'status'): 
    current_app.logger.warn("Trigger: Status attribute is not modified")
    return
  notif_pri=PRI_TASK_CHANGES
  subject="Task " + '"' + src.title + '" ' + " status changed to " + src.status
  content=subject + " URL: " + request.url_root + \
    models.Task.__tablename__ + "/" + str(src.task_group_task_id)
  workflow_owner = get_workflow_owner(src)
  if workflow_owner is None:
    current_app.logger.warn("Unable to find workflow owner for task: " + src.title)
    return
  assignee = get_assignee(src)
  if assignee is None:
    current_app.logger.warn("Unable to find assignee for task: " + src.title)
    return
  if obj.status in ['InProgress', 'Declined', 'Verified']: 
    notif_type='Email_Now'
    recipients = [assignee]
    prepare_notification(src, notif_type, notif_pri, subject, content, workflow_owner, recipients)
    #ToDo(Mouli): Avoid creating duplicate notification object, add a new notification_recipient
    if obj.status in ['Verified']: 
      notif_type='Email_Digest'
      prepare_notification(src, notif_type, notif_pri, subject, content, workflow_owner, recipients)
  if obj.status in ['Completed']: 
    notif_type='Email_Digest'
    recipients=[workflow_owner]
    prepare_notification(src, notif_type, notif_pri, subject, content, assignee, recipients)

def prepare_notification(src, notif_type, notif_pri, subject, content, owner, recipients, \
  override=False):
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
    email_notification.notify_one(notification, override)
