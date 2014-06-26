# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


from flask import current_app, request
import ggrc_workflows.models as models
from ggrc.notification import EmailNotification, EmailDigestNotification, isNotificationEnabled
from datetime import date, timedelta
from ggrc.services.common import Resource
from ggrc.models import Person
from ggrc import db

PRI_TASK_OVERDUE=1
PRI_TASK_DUE=2
PRI_TASK_ASSIGNMENT=3
PRI_TASK_CHANGES=4
PRI_OTHERS=5

def get_workflow_owner(workflow):
  if workflow.owners is not None:
    for workflow_owner in workflow.owners:
      return workflow_owner
  else:
    return None

def get_task_workflow_owner(task):
  workflow = get_workflow(task) 
  if workflow is None:
    current_app.logger.warn("Trigger: workflow object is not found")
    return None
  return get_workflow_owner(workflow)

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

def get_task_contacts(task):
  workflow_owner = get_task_workflow_owner(task)
  if workflow_owner is None:
    current_app.logger.warn("Unable to find workflow owner for task: " + task.title)
    return None
  assignee = get_assignee(task)
  if assignee is None:
    current_app.logger.warn("Unable to find assignee for task: " + task.title)
    return None
  ret_tuple=(workflow_owner, assignee)
  return ret_tuple

def prepare_notification_for_task(task, sender, recipient, subject, notif_pri):
  workflow = get_workflow(task)
  if workflow is None:
    current_app.logger.warn("Unable to find workflow for task: " + task.title)
    return
  recipients = [recipient]
  empty_line = """
  """
  content=subject + " for workflow '" + workflow.title + "' " + empty_line + \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) + "#task_widget"
  if isNotificationEnabled(recipient.id, 'Email_Now'):
    prepare_notification(task, 'Email_Now', notif_pri, subject, content, sender, recipients)
  if isNotificationEnabled(recipient.id, 'Email_Digest'):
    prepare_notification(task, 'Email_Digest', notif_pri, subject, content, sender, recipients)

def handle_tasks_overdue():
  tasks = db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date < date.today()).\
    filter(models.CycleTaskGroupObjectTask.status != 'Verified').\
    all()
  for task in tasks:
    contact = get_task_contacts(task)
    if contact is None:
      continue
    workflow_owner=contact[0]
    assignee=contact[1]
    subject="Task " + "'" + task.title + "' is past overdue " 
    prepare_notification_for_task(task, workflow_owner, assignee, subject, PRI_TASK_OVERDUE)

def handle_tasks_due(num_days):
  tasks = db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date == (date.today() + timedelta(num_days))).\
    filter(models.CycleTaskGroupObjectTask.status != 'Verified').\
    all()
  for task in tasks:
    contact = get_task_contacts(task)
    if contact is None:
      continue
    workflow_owner=contact[0]
    assignee=contact[1]
    subject="Task " + "'" + task.title + "' is due in " + str(num_days) + " days"
    prepare_notification_for_task(task, workflow_owner, assignee, subject, PRI_TASK_DUE)

@Resource.model_put.connect_via(models.CycleTaskGroupObjectTask)
def handle_task_put(sender, obj=None, src=None, service=None):
  if not getattr(obj, 'status'): 
    current_app.logger.warn("Trigger: Status attribute is not modified")
    return
  contact = get_task_contacts(obj)
  if contact is None:
    current_app.logger.warn("Trigger: Unable to get from/to contact information")
    return
  workflow_owner=contact[0]
  assignee=contact[1]
  subject="Task " + "'" + obj.title + "' status changed to " + obj.status
  if obj.status in ['InProgress', 'Assigned', 'Declined', 'Verified']: 
    prepare_notification_for_task(obj, workflow_owner, assignee, subject, PRI_TASK_CHANGES)
  if obj.status in ['Finished']: 
    prepare_notification_for_task(obj, assignee, workflow_owner, subject, PRI_TASK_CHANGES)

def prepare_notification_for_cycle(cycle, subject, notif_pri):
  workflow=db.session.query(models.Workflow).\
    filter(models.Workflow.id == cycle.workflow_id).first()
  if workflow is None:
    current_app.logger.warn("Trigger: Unable to find workflow")
    return
  workflow_owner = get_workflow_owner(workflow)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner")
    return
  content=subject + " for workflow " + "'" + workflow.title + " '" + empty_line + \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) + "#current_widget"
  recipients_email=[]
  recipients_emaildigest=[]
  for person in workflow.people:
    if isNotificationEnabled(assignee.id, 'Email_Now'):
      recipients_email.append(person)
    if isNotificationEnabled(assignee.id, 'Email_Digest'):
      recipients_emaildigest.append(person)
  if len(recipients_email) or len(recipients_emaildigest):
    if len(recipients_email):
      prepare_notification(cycle, 'Email_Now', notif_pri, subject, content, \
        workflow_owner, recipients_email)
    if len(recipients_emaildigest):
      prepare_notification(cycle, 'Email_Digest', notif_pri, subject, content, \
        workflow_owner, recipients_emaildigest)

def prepare_notification_for_cycle(cycle, subject, notif_pri):
  workflow=db.session.query(models.Workflow).\
    filter(models.Workflow.id == cycle.workflow_id).first()
  if workflow is None:
    current_app.logger.warn("Trigger: Unable to find workflow")
    return
  workflow_owner = get_workflow_owner(workflow)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner")
    return
  content=subject + " for workflow " + "'" + workflow.title + " '" + empty_line +  \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) + "#current_widget"
  recipients_email=[]
  recipients_emaildigest=[]
  for person in workflow.people:
    if isNotificationEnabled(person.id, 'Email_Now'):
      recipients_email.append(person)
    if isNotificationEnabled(person.id, 'Email_Digest'):
      recipients_emaildigest.append(person)
  if len(recipients_email) or len(recipients_emaildigest):
    if len(recipients_email):
      prepare_notification(cycle, 'Email', notif_pri, subject, content, \
        workflow_owner, recipients_email)
    if len(recipients_emaildigest):
      prepare_notification(cycle, 'Email_Digest', notif_pri, subject, content, \
        workflow_owner, recipients_emaildigest)

def handle_workflow_cycle_status_change(status):
  if status not in ['Completed', 'Verified']:
    return
  workflow_cycles= db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.status == status).all()
  for cycle in workflow_cycles:
    if status == 'Completed':
       new_status = 'Verified'
    else:
       new_status = 'Ended'
    subject="Workflow Cycle " + "'" + cycle.title + "' is ready to be "  + new_status
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def handle_workflow_cycle_started():
  workflow_cycles= db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.status == 'InProgress').\
    filter(models.Cycle.start_date == date.today()).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow Cycle " + "'" + cycle.title + "' started " + str(cycle.start_date) 
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def handle_workflow_cycle_overdue():
  workflow_cycles= db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.status != 'Completed').\
    filter(models.Cycle.end_date < date.today()).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow Cycle " + "'" + cycle.title + "' overdue " + str(cycle.end_date) 
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def handle_workflow_cycle_due(num_days):
  workflow_cycles= db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.status != 'Completed').\
    filter(models.Cycle.end_date == (date.today() + timedelta(num_days))).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow Cycle " + "'" + cycle.title + "' is due in " + str(num_days) + " days"
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def handle_workflow_cycle_starting(num_days):
  workflow_cycles= db.session.query(models.Cycle).\
    join(models.Cycle.contact).\
    filter(models.Cycle.start_date == (date.today() + timedelta(num_days))).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow Cycle " + "'" + cycle.title + "' will start in " + str(num_days) + " days"
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

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
  if override and notif_type != 'Email_Now':
    email_notification = EmailNotification()
    email_notification.notif_pri = notif_pri
    notification = email_notification.prepare([src], owner, recipients, subject, content)
    email_notification.notify_one(notification, override)
