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
from ggrc_workflows import status_change

PRI_TASK_OVERDUE=1
PRI_TASK_DUE=2
PRI_TASK_ASSIGNMENT=3
PRI_TASK_CHANGES=4
PRI_TASKGROUP=5
PRI_CYCLE=6
PRI_WORKFLOW_MEMBER_CHANGES=7

def notify_on_change(workflow):
  if workflow.notify_on_change is None:
    return False
  else:
    return workflow.notify_on_change

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

def get_cycle_workflow_owner(cycle):
  workflow=get_cycle_workflow(cycle) 
  if workflow is None:
    current_app.logger.warn("Trigger: workflow is not found for cycle" + cycle.title)
    return None
  return get_workflow_owner(workflow)

def get_task_workflow(task):
  cycle=get_cycle(task)
  if cycle is None:
    current_app.logger.warn("Trigger: cycle is not found for task " + task.title)
    return None
  return get_cycle_workflow(cycle)

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

def get_task_assignee(task):
  if task.contact is not None:
    return task.contact
  task_group=get_taskgroup(task)
  if task_group is not None and task_group.contact is not None:
    return task_group.contact
  if task_group is None:
    current_app.logger.warn("Trigger: task group for cycle is not found for task " + task.title)
    return None
  cycle=get_taskgroup_cycle(task_group)
  if cycle is not None and cycle is not None:
    return cycle.contact
  if cycle is None:
    current_app.logger.warn("Trigger: cycle is not found for task " + task.title)
    return None
   
def get_cycle(task):
  task_group=get_taskgroup(task) 
  if task_group is None:
    current_app.logger.warn("Trigger: cycle task group is not found for task " + task.title)
    return None
  return get_taskgroup_cycle(task_group)

def get_taskgroup_cycle(task_group):
  return task_group.cycle

def get_cycle_workflow(cycle):
  return cycle.workflow

def get_taskgroup(task):
  task_group_object=task.cycle_task_group_object
  if task_group_object == None:
    return None
  return task_group_object.cycle_task_group

def get_task_contacts(task):
  workflow_owner=get_task_workflow_owner(task)
  if workflow_owner is None:
    current_app.logger.warn("Unable to find workflow owner for task " + task.title)
    return None
  assignee=get_task_assignee(task)
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
  if task_group.contact is None:
    current_app.logger.warn("Trigger: Unable to find contacts for task group " + \
      task_group.title + " , using workflow owner as contact")
    ret_tuple=(workflow_owner, workflow_owner)
  else:
    contacts=task_group.contact
    if contacts is None:
      current_app.logger.warn("Trigger: Unable to find contact information for task group " + task_group.title)
      return None
    ret_tuple=(workflow_owner, contacts)
  return ret_tuple

def get_cycle_contacts(cycle):
  workflow_owner=get_cycle_workflow_owner(cycle)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner for cycle" + cycle.title)
    return None
  if cycle.contact is None:
    current_app.logger.warn("Trigger: Unable to find contacts for cycle " + \
      cycle.title + " , using workflow owner as contact")
    ret_tuple=(workflow_owner, workflow_owner)
  else:
    contacts=cycle.contact
    if contacts is None:
      current_app.logger.warn("Trigger: Unable to find contact information for cycle" + cycle.title)
      return None
    ret_tuple=(workflow_owner, contacts)
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
  override_flag=notify_on_change(workflow)
  prepare_notification(task, 'Email_Now', notif_pri, subject, content, sender, recipients, override=override_flag)
  prepare_notification(task, 'Email_Digest', notif_pri, subject, content, sender, recipients, override=override_flag)

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
  override_flag=notify_on_change(workflow)
  prepare_notification(task_group, 'Email_Now', notif_pri, subject, content, sender, recipients, override=override_flag)
  prepare_notification(task_group, 'Email_Digest', notif_pri, subject, content, sender, recipients, override=override_flag)

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

@status_change.connect_via(models.Cycle)
def handle_cycle_status_change(sender, obj=None, new_status=None, old_status=None):
  if obj is None:
    current_app.logger.warn("Trigger: Unable to get cycle object")
    return
  contact=get_cycle_contacts(obj)
  if contact is None:
    current_app.logger.warn("Trigger: Unable to get cycle contact information")
    return
  notify_custom_message=False
  if new_status in ['InProgress']:
    notify_custom_message=True
    subject="Workflow Cycle " + "'" + obj.title + "' started, status set to InProgress"
  else:
    subject="Workflow Cycle " + "'" + obj.title + "' status changed to "  + new_status
  prepare_notification_for_cycle(obj, subject, PRI_CYCLE, notify_custom_message)

@status_change.connect_via(models.CycleTaskGroup)
def handle_taskgroup_status_change(sender, obj=None, new_status=None, old_status=None):
  if obj is None:
    current_app.logger.warn("Trigger: Unable to get task group object")
    return
  contact=get_task_group_contacts(obj)
  if contact is None:
    current_app.logger.warn("Trigger: Unable to get task group contact information")
    return
  workflow_owner=contact[0]
  assignee=contact[1]
  subject="Task Group " + "'" + obj.title + "' status changed to "  + new_status
  prepare_notification_for_taskgroup(obj, workflow_owner, assignee, subject, PRI_TASKGROUP)

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

@Resource.model_posted.connect_via(models.WorkflowPerson)
def handle_workflow_person_post(sender, obj=None, src=None, service=None):
  person=obj.person
  workflow=obj.workflow
  subject="Member " + person.name + " is added to workflow " + workflow.title
  prepare_notification_for_workflow_member(workflow, person, subject, PRI_WORKFLOW_MEMBER_CHANGES, 'Add')

@Resource.model_deleted.connect_via(models.WorkflowPerson)
def handle_workflow_person_deleted(sender, obj=None, service=None):
  person=obj.person
  workflow=obj.workflow
  subject="Member " + person.name + " is removed from workflow " + workflow.title
  prepare_notification_for_workflow_member(workflow, person, subject, PRI_WORKFLOW_MEMBER_CHANGES, 'Remove')

def prepare_notification_for_workflow_member(workflow, member, subject, notif_pri, action):
  if not action in ['Add', 'Remove']:
    return
  found_cycle=False
  for cycle in workflow.cycles:
    if cycle.status not in ['InProgress', 'Finished', 'Verified']:
      continue
    else:
      found_cycle=True
      break
  if not found_cycle:
    current_app.logger.warn("Trigger: No Cycle has been started for workflow " + workflow.title)
    return
  workflow_owner=get_workflow_owner(workflow)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner")
    return
  override_flag=notify_on_change(workflow)
  empty_line="""
  """
  content=empty_line + subject + empty_line +  \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) + "#person_widget"
  to_email={}
  # custom message is set in email for new member added to workflow (not for email digest)
  if action in ['Add']:
    notify_custom_message={member.id: workflow.notify_custom_message}
  else:
    notify_custom_message=None
  recipients=[]
  for person in workflow.people:
    if not to_email.has_key(person.id):
      to_email[person.id]=True
      recipients.append(person)
  if len(recipients):
    prepare_notification(workflow, 'Email_Now', notif_pri, subject, content, \
      workflow_owner, recipients, notify_custom_message=notify_custom_message, override=override_flag)
    prepare_notification(workflow, 'Email_Digest', notif_pri, subject, content, \
        workflow_owner, recipients, override=override_flag)

def prepare_notification_for_cycle(cycle, subject, notif_pri, notify_custom_message=False):
  workflow=get_cycle_workflow(cycle)
  if workflow is None:
    current_app.logger.warn("Trigger: Unable to find workflow for cycle")
    return
  workflow_owner=get_workflow_owner(workflow)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner for cycle")
    return
  override_flag=notify_on_change(workflow)
  empty_line="""
  """
  content=empty_line + subject + empty_line +  \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) + "#current_widget"
  email_content=content
  if notify_custom_message is True and workflow.notify_custom_message is not None:
    email_content=workflow.notify_custom_message + empty_line + content
  prepare_notification(cycle, 'Email_Now', notif_pri, subject, email_content, \
    workflow_owner, workflow.people, override=override_flag)
  prepare_notification(cycle, 'Email_Digest', notif_pri, subject, content, \
    workflow_owner, workflow.people, override=override_flag)

def handle_workflow_cycle_overdue():
  workflow_cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.status != 'Finished').\
    filter(models.Cycle.status != 'Verified').\
    filter(models.Cycle.end_date < date.today()).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow " + "'" + cycle.title + "' is past overdue " + str(cycle.end_date) 
    prepare_notification_for_cycle(cycle, subject, PRI_CYCLE)

def handle_workflow_cycle_due(num_days):
  workflow_cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.status != 'Finished').\
    filter(models.Cycle.status != 'Verified').\
    filter(models.Cycle.end_date == (date.today() + timedelta(num_days))).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow " + "'" + cycle.title + "' is due in " + str(num_days) + " days"
    prepare_notification_for_cycle(cycle, subject, PRI_CYCLE)

def handle_workflow_cycle_starting(num_days):
  workflow_cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.status != 'Finished').\
    filter(models.Cycle.status != 'Verified').\
    filter(models.Cycle.start_date == (date.today() + timedelta(num_days))).\
    all()
  for cycle in workflow_cycles:
    subject="Workflow " + "'" + cycle.title + "' will start in " + str(num_days) + " days"
    prepare_notification_for_cycle(cycle, subject, PRI_CYCLE)

def prepare_notification(src, notif_type, notif_pri, subject, content, owner, recipients, \
  override=False, notify_custom_message=None):
  if notif_type == 'Email_Digest':
    #ToDo(Mouli): Additional checks for recipients prior to preparing email digest
    emaildigest_notification = EmailDigestNotification()
    emaildigest_notification.notif_pri = notif_pri
    emaildigest_notification.prepare([src], owner, recipients, subject, content, override)
  elif notif_type == 'Email_Now':
    email_notification=EmailNotification()
    email_notification.notif_pri=notif_pri
    notification=email_notification.prepare([src], owner, recipients, subject, content, override)
    if notification is not None:
      email_notification.notify_one(notification, notify_custom_message)
  else:
    return None
