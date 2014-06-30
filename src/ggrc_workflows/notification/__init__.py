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
  workflow=get_task_workflow(task) 
  if workflow is None:
    current_app.logger.warn("Trigger: workflow is not found for task " + task.title)
    return None
  return get_workflow_owner(workflow)

def get_taskgroup_workflow_owner(task_group):
  workflow=get_taskgroup_workflow(task_group) 
  if workflow is None:
    current_app.logger.warn("Trigger: workflow is not found for task group " + task_group.title)
    return None
  return get_workflow_owner(workflow)

def get_task_workflow(task):
  cycle=get_cycle(task)
  if cycle is None:
    current_app.logger.warn("Trigger: cycle is not found for task " + task.title)
    return None
  return db.session.query(models.Workflow).\
    filter(models.Workflow.id == cycle.workflow_id).first()

def get_taskgroup_workflow(task_group):
  cycle=get_taskgroup_cycle(task_group) 
  if cycle is None:
    current_app.logger.warn("Trigger: cycle is not found for task group " + task_group.title)
    return None
  workflow=get_cycle_workflow(cycle)
  if workflow is None:
    current_app.logger.warn("Trigger: workflow cycle is not found for task group " + task_group.title)
    return None
  return workflow

def get_assignee(task):
  if task.contact_id is not None:
    return db.session.query(Person).filter(Person.id==task.contact_id).first()
  task_group=get_taskgroup(task)
  if task_group is not None and task_group.contact_id is not None:
    return db.session.query(Person).filter(Person.id==task_group.contact_id).first()
  if task_group is None:
    current_app.logger.warn("Trigger: task group for cycle is not found for task " + task.title)
    return None
  cycle=get_taskgroup_cycle(task_group)
  if cycle is not None and cycle.contact_id is not None:
    return db.session.query(Person).filter(Person.id==cycle.contact_id).first()
  if cycle is None:
    current_app.logger.warn("Trigger: cycle is not found for task " + task.title)
    return None
   
def get_cycle(task):
  task_group=get_taskgroup(task) 
  if task_group is None:
    current_app.logger.warn("Trigger: cycle task group is not found for task " + task.title)
    return None
  return db.session.query(models.Cycle).\
    filter(models.Cycle.id == task_group.cycle_id).first()

def get_taskgroup_cycle(task_group):
  return db.session.query(models.Cycle).\
    filter(models.Cycle.id == task_group.cycle_id).first()

def get_cycle_workflow(cycle):
  workflow=db.session.query(models.Workflow).\
    filter(models.Workflow.id == cycle.workflow_id).first()
  return workflow

def get_taskgroup_object(task):
  task_group_object=db.session.query(models.CycleTaskGroupObject).\
    filter(models.CycleTaskGroupObject.id == task.cycle_task_group_object_id).first()
  return task_group_object

def get_taskgroup(task):
  task_group_object=get_taskgroup_object(task)
  if task_group_object == None:
    return None
  task_group=db.session.query(models.CycleTaskGroup).\
    filter(models.CycleTaskGroup.id == task_group_object.cycle_task_group_id).first()
  return task_group

def get_task_contacts(task):
  workflow_owner=get_task_workflow_owner(task)
  if workflow_owner is None:
    current_app.logger.warn("Unable to find workflow owner for task " + task.title)
    return None
  assignee=get_assignee(task)
  if assignee is None:
    current_app.logger.warn("Trigger: Unable to find assignee for task " + task.title)
    return None
  ret_tuple=(workflow_owner, assignee)
  return ret_tuple

def get_task_group_contacts(task_group):
  workflow_owner=get_taskgroup_workflow_owner(task_group)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner for task group " + task_group.title)
    return None
  ret_tuple=(workflow_owner, workflow_owner)
  return ret_tuple

def prepare_notification_for_task(task, sender, recipient, subject, notif_pri):
  workflow=get_task_workflow(task)
  if workflow is None:
    current_app.logger.warn("Trigger: Unable to find workflow for task " + task.title)
    return
  recipients=[recipient]
  empty_line="""
  """
  content=empty_line + subject + " for workflow '" + workflow.title + "' " + empty_line + \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) + "#task_widget"
  if isNotificationEnabled(recipient.id, 'Email_Now'):
    prepare_notification(task, 'Email_Now', notif_pri, subject, content, sender, recipients)
  if isNotificationEnabled(recipient.id, 'Email_Digest'):
    prepare_notification(task, 'Email_Digest', notif_pri, subject, content, sender, recipients)

def prepare_notification_for_taskgroup(task_group, sender, recipient, subject, notif_pri):
  workflow=get_taskgroup_workflow(task_group)
  if workflow is None:
    current_app.logger.warn("Trigger: Unable to find workflow for task group " + task_group.title)
    return
  recipients=[recipient]
  empty_line="""
  """
  content=empty_line + subject + " for workflow '" + workflow.title + "' " + empty_line + \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) + "#task_group_widget"
  if isNotificationEnabled(recipient.id, 'Email_Now'):
    prepare_notification(task_group, 'Email_Now', notif_pri, subject, content, sender, recipients)
  if isNotificationEnabled(recipient.id, 'Email_Digest'):
    prepare_notification(task_group, 'Email_Digest', notif_pri, subject, content, sender, recipients)

def handle_tasks_overdue():
  tasks=db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date < date.today()).\
    filter(models.CycleTaskGroupObjectTask.status != 'Finished').\
    filter(models.CycleTaskGroupObjectTask.status != 'Verified').\
    all()
  for task in tasks:
    contact=get_task_contacts(task)
    if contact is None:
      continue
    workflow_owner=contact[0]
    assignee=contact[1]
    subject="Task " + "'" + task.title + "' is past overdue "  + str(task.end_date)
    prepare_notification_for_task(task, workflow_owner, assignee, subject, PRI_TASK_OVERDUE)

def handle_task_group_status_change(status):
  if status not in ['Finished']:
    return
  task_groups=db.session.query(models.CycleTaskGroup).\
    filter(models.CycleTaskGroup.status == status).\
    filter(models.CycleTaskGroup.end_date > date.today()).\
    all()
  for task_group in task_groups:
    contact=get_task_group_contacts(task_group)
    if contact is None:
      continue
    workflow_owner=contact[0]
    assignee=contact[1]
    subject="Task Group " + "'" + task_group.title + "' status changed to "  + status
    prepare_notification_for_taskgroup(task_group, workflow_owner, assignee, subject, PRI_OTHERS)

def handle_tasks_due(num_days):
  tasks=db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date == (date.today() + timedelta(num_days))).\
    filter(models.CycleTaskGroupObjectTask.status != 'Finished').\
    filter(models.CycleTaskGroupObjectTask.status != 'Verified').\
    all()
  for task in tasks:
    contact=get_task_contacts(task)
    if contact is None:
      continue
    workflow_owner=contact[0]
    assignee=contact[1]
    subject="Task " + "'" + task.title + "' is due in " + str(num_days) + " days"
    prepare_notification_for_task(task, workflow_owner, assignee, subject, PRI_TASK_DUE)

@Resource.model_put.connect_via(models.CycleTaskGroupObjectTask)
def handle_task_put(sender, obj=None, src=None, service=None):
  if not (src.get('status') and getattr(obj, 'status')):
    current_app.logger.warn("Trigger: Status attribute is not modified for task")
    return
  contact=get_task_contacts(obj)
  if contact is None:
    current_app.logger.warn("Trigger: Unable to get task contact information")
    return
  workflow_owner=contact[0]
  assignee=contact[1]
  subject="Task " + "'" + obj.title + "' status changed to " + obj.status
  notif_pri=PRI_TASK_CHANGES
  if obj.status in ['InProgress']:
    notif_pri=PRI_TASK_ASSIGNMENT
  if obj.status in ['InProgress', 'Assigned', 'Declined', 'Verified']: 
    prepare_notification_for_task(obj, workflow_owner, assignee, subject, notif_pri)
  if obj.status in ['Finished']: 
    prepare_notification_for_task(obj, assignee, workflow_owner, subject, notif_pri)

@Resource.model_posted.connect_via(models.WorkflowPerson)
def handle_workflow_person_post(sender, obj=None, src=None, service=None):
  person=obj.person
  workflow=obj.workflow
  subject="Member " + person.name + " is added to workflow " + workflow.title
  prepare_notification_for_workflow_member(workflow, person, subject, PRI_OTHERS)

@Resource.model_deleted.connect_via(models.WorkflowPerson)
def handle_workflow_person_deleted(sender, obj=None, service=None):
  person=obj.person
  workflow=obj.workflow
  subject="Member " + person.name + " is removed from workflow " + workflow.title
  prepare_notification_for_workflow_member(workflow, person, subject, PRI_OTHERS)

def prepare_notification_for_workflow_member(workflow, member, subject, notif_pri):
  workflow_owner=get_workflow_owner(workflow)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner")
    return
  empty_line="""
  """
  content=empty_line + subject + empty_line +  \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) 
  recipients_email=[]
  recipients_emaildigest=[]
  if isNotificationEnabled(member.id, 'Email_Now'):
    recipients_email.append(member)
  if isNotificationEnabled(member.id, 'Email_Digest'):
    recipients_emaildigest.append(member)
  for person in workflow.people:
    if isNotificationEnabled(person.id, 'Email_Now'):
      recipients_email.append(person)
    if isNotificationEnabled(person.id, 'Email_Digest'):
      recipients_emaildigest.append(person)
  if len(recipients_email) or len(recipients_emaildigest):
    if len(recipients_email):
      prepare_notification(workflow, 'Email', notif_pri, subject, content, \
        workflow_owner, recipients_email)
    if len(recipients_emaildigest):
      prepare_notification(workflow, 'Email_Digest', notif_pri, subject, content, \
        workflow_owner, recipients_emaildigest)

def prepare_notification_for_cycle(cycle, subject, notif_pri):
  workflow=db.session.query(models.Workflow).\
    filter(models.Workflow.id == cycle.workflow_id).first()
  if workflow is None:
    current_app.logger.warn("Trigger: Unable to find workflow for cycle")
    return
  workflow_owner=get_workflow_owner(workflow)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner for cycle")
    return
  empty_line="""
  """
  content=empty_line + subject + empty_line +  \
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
  if status not in ['InProgress', 'Finished']:
    return
  workflow_cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.status == status).\
    filter(models.Cycle.end_date > date.today()).\
    all()
  for cycle in workflow_cycles:
    if status == 'InProgress':
       new_status='Finished'
    elif status == 'Finished':
       new_status='Verified'
    else:
      continue
    subject="Workflow " + "'" + cycle.title + "' is ready to be "  + new_status
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def handle_workflow_cycle_started():
  workflow_cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.status == 'InProgress').\
    filter(models.Cycle.start_date == date.today()).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow " + "'" + cycle.title + "' started " + str(cycle.start_date) 
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def handle_workflow_cycle_overdue():
  workflow_cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.status != 'Finished').\
    filter(models.Cycle.status != 'Verified').\
    filter(models.Cycle.end_date < date.today()).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow " + "'" + cycle.title + "' is past overdue " + str(cycle.end_date) 
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def handle_workflow_cycle_due(num_days):
  workflow_cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.status != 'Finished').\
    filter(models.Cycle.status != 'Verified').\
    filter(models.Cycle.end_date == (date.today() + timedelta(num_days))).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow " + "'" + cycle.title + "' is due in " + str(num_days) + " days"
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def handle_workflow_cycle_starting(num_days):
  workflow_cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.status != 'Finished').\
    filter(models.Cycle.status != 'Verified').\
    filter(models.Cycle.start_date == (date.today() + timedelta(num_days))).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow " + "'" + cycle.title + "' will start in " + str(num_days) + " days"
    prepare_notification_for_cycle(cycle, subject, PRI_OTHERS)

def prepare_notification(src, notif_type, notif_pri, subject, content, owner, recipients, \
  override=False):
  if notif_type == 'Email_Digest':
    emaildigest_notification = EmailDigestNotification()
    emaildigest_notification.notif_pri = notif_pri
    emaildigest_notification.prepare([src], owner, recipients, subject, content)
  elif notif_type == 'Email_Now':
    email_notification=EmailNotification()
    email_notification.notif_pri=notif_pri
    notification=email_notification.prepare([src], owner, recipients, subject, content)
    email_notification.notify_one(notification)
  else:
    return None
  if override and notif_type != 'Email_Now':
    email_notification=EmailNotification()
    email_notification.notif_pri=notif_pri
    notification=email_notification.prepare([src], owner, recipients, subject, content)
    email_notification.notify_one(notification, override)
