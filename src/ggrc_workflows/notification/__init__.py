# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


from flask import current_app, request
from ggrc.app import app
import ggrc_workflows.models as models
from ggrc.notification import EmailNotification, EmailDigestNotification
from ggrc.notification import EmailDeferredNotification, EmailDigestDeferredNotification
from ggrc.notification import CalendarNotification, CalendarService, GGRC_CALENDAR
from ggrc.notification import create_calendar_entry, find_calendar_entry, get_calendar_event
from ggrc.notification import create_calendar_acls, delete_calendar_event
from datetime import date, timedelta
from ggrc.services.common import Resource
from ggrc.models import Person, NotificationConfig
from ggrc_basic_permissions.models import Role, UserRole
from ggrc import db
from ggrc import settings
from ggrc_workflows import status_change, workflow_cycle_start
from datetime import datetime
from werkzeug.exceptions import Forbidden
from ggrc.login import get_current_user
#from ggrc_workflows import calc_start_date

PRI_TASK_OVERDUE=1
PRI_TASK_DUE=2
PRI_TASK_ASSIGNMENT=3
PRI_TASK_CHANGES=4
PRI_TASKGROUP=5
PRI_WORKFLOW=6
PRI_CYCLE=7
PRI_WORKFLOW_MEMBER_CHANGES=8
PRI_OTHERS=9

WORKFLOW_CYCLE_DUE=3
WORKFLOW_CYCLE_STARTING=[3, 7]

def notify_on_change(workflow):
  if workflow.notify_on_change is None:
    return False
  else:
    return workflow.notify_on_change

def get_cycle_by_id(id):
  return db.session.query(models.Cycle).\
    filter(models.Cycle.id == id).first()

def get_taskgroup_by_id(id):
  return db.session.query(models.CycleTaskGroup).\
    filter(models.CycleTaskGroup.id == id).first()

def get_workflow_owner(workflow):
  workflow_owner_role = Role.query.filter(Role.name == 'WorkflowOwner').first()
  user_roles = UserRole.query.filter(
      UserRole.context_id == workflow.context_id,
      UserRole.role_id == workflow_owner_role.id)
  for user_role in user_roles:
    return user_role.person

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
  ret_tuple=(workflow_owner, workflow_owner)
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
  prepare_notification(task, 'Email_Deferred', notif_pri, subject, content, sender, \
   recipients, override=override_flag)
  prepare_notification(task, 'Email_Digest_Deferred', notif_pri, subject, content, sender, \
   recipients, override=override_flag)

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
  prepare_notification(task_group, 'Email_Deferred', notif_pri, subject, content, sender, recipients, override=override_flag)
  prepare_notification(task_group, 'Email_Digest_Deferred', notif_pri, subject, content, sender, recipients, override=override_flag)

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

@Resource.model_posted.connect_via(NotificationConfig)
def handle_notification_config_post(sender, obj=None, src=None, service=None):
   handle_notification_config_changes(sender, obj, src, service)

@Resource.model_put.connect_via(NotificationConfig)
def handle_notification_config_put(sender, obj=None, src=None, service=None):
   handle_notification_config_changes(sender, obj, src, service)

def handle_notification_config_changes(sender, obj=None, src=None, service=None):
  if obj.notif_type != 'Calendar':
    return
  cycles=db.session.query(models.Cycle).\
    filter(models.Cycle.is_current==True).all()
  user=get_current_user()
  for cycle in cycles:
    workflow=get_cycle_workflow(cycle)
    workflow_owner=get_workflow_owner(workflow)
    assignees=[]
    for person in workflow.people:
      assignees.append(person)
    assignees.append(workflow_owner)
    for assignee in assignees:
      if assignee.id == user.id:
        enable_flag={assignee.id: obj.enable_flag}
        prepare_calendar_for_cycle(cycle, enable_flag)

@Resource.model_put.connect_via(models.Cycle)
def handle_end_cycle(sender, obj=None, src=None, service=None):
  if obj is None:
    current_app.logger.warn("Trigger: Unable to get cycle object")
    return
  if not hasattr(obj, 'is_current'):
    current_app.logger.warn("is_current attribute is not set in object")
    return
  if not obj.is_current:
    notify_custom_message=False
    subject="Workflow Cycle " + "'" + obj.title + "' ended"
    prepare_notification_for_cycle(obj, subject, PRI_CYCLE, notify_custom_message)

@workflow_cycle_start.connect_via(models.Cycle)
def handle_start_cycle(sender, obj=None, new_status=None, old_status=None):
  if obj is None:
    current_app.logger.warn("Trigger: Unable to get cycle object")
    return
  notify_custom_message=True
  subject="Workflow Cycle " + "'" + obj.title + "' started"
  prepare_notification_for_cycle(obj, subject, PRI_CYCLE, notify_custom_message)
  prepare_calendar_for_cycle(obj)

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

@Resource.model_deleted.connect_via(models.CycleTaskGroup)
def handle_taskgroup_deleted(sender, obj=None, service=None):
  if request.oauth_credentials is None:
    raise Forbidden()
  from oauth2client.client import Credentials
  calendar_service=WorkflowCalendarService(Credentials.new_from_json(request.oauth_credentials))
  calendar_service.handle_taskgroup_calendar_delete(taskgroup)

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
  user=get_current_user()
  if obj.status in ['InProgress', 'Finished', 'Assigned', 'Declined', 'Verified']: 
    prepare_notification_for_task(obj, user, assignee, subject, notif_pri)
    taskgroup=get_taskgroup(obj)
    if taskgroup is not None:
      prepare_calendar_for_taskgroup(taskgroup)
    else:
      current_app.logger.warn("Trigger: Unable to get task group for task " + obj.title)

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
    notify_custom_message={member.id: workflow.notify_custom_message + '<br>'}
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
    prepare_calendar_for_workflow_member(workflow, member)

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
    email_content=workflow.notify_custom_message + "<br>" + content
  prepare_notification(cycle, 'Email_Now', notif_pri, subject, email_content, \
    workflow_owner, workflow.people, override=override_flag)
  prepare_notification(cycle, 'Email_Digest', notif_pri, subject, content, \
    workflow_owner, workflow.people, override=override_flag)

def prepare_notification_for_workflow(workflow, subject, notif_pri):
  workflow_owner=get_workflow_owner(workflow)
  if workflow_owner is None:
    current_app.logger.warn("Trigger: Unable to find workflow owner for cycle")
    return
  override_flag=notify_on_change(workflow)
  empty_line="""
  """
  content=empty_line + subject + empty_line +  \
    "  " + request.url_root + workflow._inflector.table_plural + \
    "/" + str(workflow.id) + "#info_widget"
  prepare_notification(workflow, 'Email_Now', notif_pri, subject, content, \
    workflow_owner, workflow.people, override=override_flag)
  prepare_notification(workflow, 'Email_Digest', notif_pri, subject, content, \
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
  workflows=db.session.query(models.Workflow)
  for workflow in workflows:
    next_start_date = workflow.next_cycle_start_date
    #next_start_date=calc_start_date(
    #  workflow.frequency, 
    #  workflow.start_date)
    starting_date=date.today() + timedelta(num_days)
    if next_start_date == starting_date:
      subject="Workflow " + "'" + workflow.title + "' will start in " + str(num_days) + " days"
      prepare_notification_for_workflow(workflow, subject, PRI_WORKFLOW)

def prepare_notification(src, notif_type, notif_pri, subject, content, owner, recipients, \
  override=False, notify_custom_message=None):
  if notif_type == 'Email_Digest':
    emaildigest_notification = EmailDigestNotification()
    emaildigest_notification.notif_pri = notif_pri
    try:
      emaildigest_notification.prepare([src], owner, recipients, subject, content, override)
    except Exception as e:
      current_app.logger.warn("Exception occured in preparing email digest notification: " + str(e))
  elif notif_type == 'Email_Digest_Deferred':
    emaildigest_notification = EmailDigestDeferredNotification()
    emaildigest_notification.notif_pri = notif_pri
    try:
      emaildigest_notification.prepare([src], owner, recipients, subject, content, override)
    except Exception as e:
      current_app.logger.warn("Exception occured in preparing deferred email digest notification: " + str(e))
  elif notif_type == 'Email_Now':
    email_notification=EmailNotification()
    email_notification.notif_pri=notif_pri
    try:
      notification=email_notification.prepare([src], owner, recipients, subject, content, override)
    except Exception as e:
      current_app.logger.warn("Exception occured in preparing email notification: " + str(e))
      return
    if notification is not None:
      try:
        email_notification.notify_one(notification, notify_custom_message)
      except Exception as e:
        current_app.logger.warn("Exception occured in notifying email: " + str(e))
  elif notif_type == 'Email_Deferred':
    try:
      email_notification=EmailDeferredNotification()
      email_notification.notif_pri=notif_pri
      notification=email_notification.prepare([src], owner, recipients, subject, content, override)
    except Exception as e:
      current_app.logger.warn("Exception occured in preparing deferred email notification: " + str(e))

class WorkflowCalendarService(CalendarService):
  def __init__(self, credentials=None):
    super(WorkflowCalendarService, self).__init__(credentials)

  def handle_cycle_calendar_update(self, cycle, enable_flag=None):
    workflow=get_cycle_workflow(cycle)
    if workflow is None:
      current_app.logger.warn("Workflow not found for cycle " + cycle.title)
      return 
    workflow_owner=get_workflow_owner(workflow)
    if workflow_owner is None:
      current_app.logger.warn("Workflow owner not found for workflow " + workflow.title)
      return
    calendar=find_calendar_entry(self.calendar_service, GGRC_CALENDAR, workflow_owner.id)
    user=get_current_user()
    if calendar is None and user.id != workflow_owner.id:
      current_app.logger.warn("Workflow owner and super user roles can create Calendar")
      return
    if calendar is None: 
      calendar=create_calendar_entry(self.calendar_service, GGRC_CALENDAR, workflow_owner.id)
      if calendar is None:
        current_app.logger.error("Unable to create calendar entry for workflow " + workflow.title)
        raise Forbidden()
    calendar_event=get_calendar_event(self.calendar_service, calendar['id'], cycle.title)
    subject=cycle.title
    content=cycle.title + ' ' + request.url_root + workflow._inflector.table_plural + \
      '/' + str(workflow.id) + '#current_widget'
    notif=CalendarNotification()
    notif.start_date=cycle.start_date
    notif.end_date=cycle.end_date
    notif.notif_pri=PRI_OTHERS
    notif.calendar_service=self.calendar_service
    notif.calendar_event=calendar_event
    notif.calendar=calendar
    notif.enable_flag=enable_flag
    assignees=[]
    assignee_emails=[]
    for workflow_person in workflow.people:
      assignees.append(workflow_person)
      assignee_emails.append(workflow_person.email)
    #ToDo(Mouli): WF owner and Super user can update Acl
    if user.id == workflow_owner.id:
      calendar_acls=create_calendar_acls(
        self.calendar_service,
        calendar['id'],
        assignee_emails,
        [workflow_owner.email],
        'writer')
      if calendar_acls is None:
        current.logger.error("Unable to create ACLs for workflow "  + workflow.title)
        raise Forbidden()
    calendar_notification = notif.prepare([cycle], workflow_owner, assignees, subject, content)
    if calendar_notification is not None:
      notif.notify_one(calendar_notification)
    # create task group related events during start of workflow
    for task_group in cycle.cycle_task_groups:
      self.handle_taskgroup_calendar_update(task_group, calendar=calendar, enable_flag=enable_flag)

  def handle_taskgroup_calendar_update(self, task_group, calendar=None, assignee=None, enable_flag=None):
    workflow=get_taskgroup_workflow(task_group)
    if workflow is None:
      current_app.logger.warn("Workflow not found for task group " + task_group.title)
      return 
    cycle=get_taskgroup_cycle(task_group)
    if cycle is None:
      current_app.logger.warn("cycle not found for task group " + task_group.title)
      return 
    workflow_owner=get_workflow_owner(workflow)
    if workflow_owner is None:
      current_app.logger.warn("Workflow owner not found for workflow " + workflow.title)
      return
    recipient_contacts={}
    assignees=[]
    assignee_emails=[]
    for task_group_object in task_group.cycle_task_group_objects:
      for task in task_group_object.cycle_task_group_object_tasks:
        if task.contact is not None:
          recipient_contacts[task.contact.id] = task.contact
    for id, contact in recipient_contacts.items():
      assignees.append(contact)
      assignee_emails.append(contact.email)
    user=get_current_user()
    if calendar is None:
      calendar=find_calendar_entry(self.calendar_service, GGRC_CALENDAR, workflow_owner.id)
      #ToDo(Mouli): WF owners and Superuser role can update Acl
      if calendar is None and user.id != workflow_owner.id:
        current_app.logger.error("No calendar entry is created for workflow " + workflow.title)
        return
      if calendar is None:
        calendar=create_calendar_entry(self.calendar_service, GGRC_CALENDAR, workflow_owner.id)
        if calendar is None:
          current_app.logger.error("Unable to create calendar entry for workflow " + workflow.title)
          raise Forbidden()
    calendar_event=get_calendar_event(self.calendar_service, calendar['id'], task_group.title)
    subject=task_group.title
    content=task_group.title + ' ' + request.url_root + workflow._inflector.table_plural + \
      '/' + str(workflow.id) + '#task_group_widget'
    notif=CalendarNotification()
    if task_group.start_date is None:
      notif.start_date=cycle.start_date
    else:
      notif.start_date=task_group.start_date
    if task_group.end_date is None:
      notif.end_date=cycle.end_date
    else:
      notif.end_date=task_group.end_date
    notif.notif_pri=PRI_OTHERS
    notif.calendar_service=self.calendar_service
    notif.calendar_event=calendar_event
    notif.calendar=calendar
    notif.enable_flag=enable_flag
    #ToDo(Mouli): WF owner and Super user can update Acl
    if user.id == workflow_owner.id:
      calendar_acls=create_calendar_acls(
        self.calendar_service,
        calendar['id'],
        assignee_emails,
        [workflow_owner.email],
        'writer')
      if calendar_acls is None:
        current.logger.error("Unable to create ACLs for workflow "  + workflow.title)
        raise Forbidden()
    calendar_notification = notif.prepare([task_group], workflow_owner, assignees, subject, content)
    if calendar_notification is not None:
      notif.notify_one(calendar_notification)

  def handle_taskgroup_calendar_delete(self, task_group):
    workflow=get_taskgroup_workflow(task_group)
    if workflow is None:
      current_app.logger.warn("Workflow not found for task group " + task_group.title)
      return 
    workflow_owner=get_workflow_owner(workflow)
    if workflow_owner is None:
      current_app.logger.warn("Workflow owner not found for workflow " + workflow.title)
      return
    user=get_current_user()
    calendar=find_calendar_entry(self.calendar_service, GGRC_CALENDAR, workflow_owner.id)
    if calendar is None:
      current_app.logger.error("No calendar entry is created for workflow " + workflow.title)
      return
    calendar_event=get_calendar_event(self.calendar_service, calendar['id'], task_group.title)
    if calendar_event is None:
      current_app.logger.warn("Calendar event could not be found for task group " + task_group.title)
      return
    #ToDo(Mouli): Create notification object similar to other calendar events such as create, update
    delete_calendar_event(self.calendar_service, calendar['id'], calendar_event['id'])

def notify_email_digest():
  """ Preprocessing of tasks, cycles prior to generating email digest
  """
  handle_tasks_overdue()
  handle_workflow_cycle_overdue()
  handle_workflow_cycle_due(WORKFLOW_CYCLE_DUE)
  for num_days in WORKFLOW_CYCLE_STARTING:
    handle_workflow_cycle_starting(num_days)
  db.session.commit()

  email_digest_notification=EmailDigestNotification()
  email_digest_notification.notify()
  db.session.commit()

def notify_email_deferred():
  """ Processing of deferred emails in particular handling Task/Undo 
  """
  email_deferred=EmailDeferredNotification()
  email_deferred.notify()
  db.session.commit()

  """ Processing of deferred email digest in particular handling Task/Undo 
      Marking notification type to be EmailDigest
  """
  email_digest_deferred=EmailDigestDeferredNotification()
  email_digest_deferred.notify()
  db.session.commit()

def prepare_calendar_for_cycle(cycle, enable_flag=None):
  if request.oauth_credentials is None:
    raise Forbidden()
  from oauth2client.client import Credentials
  calendar_service=WorkflowCalendarService(Credentials.new_from_json(request.oauth_credentials))
  calendar_service.handle_cycle_calendar_update(cycle, enable_flag)

def prepare_calendar_for_workflow_member(workflow, member):
  if request.oauth_credentials is None:
    raise Forbidden()
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
  from oauth2client.client import Credentials
  calendar_service=WorkflowCalendarService(Credentials.new_from_json(request.oauth_credentials))
  calendar_service.handle_cycle_calendar_update(cycle)

def prepare_calendar_for_taskgroup(taskgroup, assignee=None):
  if request.oauth_credentials is None:
    raise Forbidden()
  from oauth2client.client import Credentials
  calendar_service=WorkflowCalendarService(Credentials.new_from_json(request.oauth_credentials))
  calendar_service.handle_taskgroup_calendar_update(taskgroup, assignee=assignee)
