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
    filter(models.CycleTaskGroupObjectTask.end_date < date.today()).all()
  for task in tasks:
    subject="Task " + '"' + task.title + '" ' + "is past overdue " 
    content="Task " + task.title + " : " + request.url_root + models.Task.__tablename__ + \
      "/" + str(task.task_group_task_id) + " due on " + str(task.end_date)
    notif_type = 'Email_Digest'
    if task.contact_id is None:
      current_app.logger.info("Trigger: Contact attribute is not set")
      continue 
    contact = db.session.query(Person).filter(Person.id == task.contact_id).first()
    if contact is None:
      current_app.logger.info("Trigger: Unable to find Contact")
      continue 
    recipients = [contact]
    notif_pri = PRI_TASK_OVERDUE
    prepare_notification(task, notif_type, notif_pri, subject, content, contact, recipients)

def handle_tasks_due(num_days):
  tasks = db.session.query(models.CycleTaskGroupObjectTask).\
    filter(models.CycleTaskGroupObjectTask.end_date < (date.today()+timedelta(num_days))).all()
  for task in tasks:
    subject="Task " + '"' + task.title + '" ' + "is due in " + str(days) + " days"
    content="Task " + task.title + " : " + request.url_root + models.Task.__tablename__ + \
      "/" + str(task.task_group_task_id) + " due on " + str(task.end_date)
    notif_type = 'Email_Digest'
    if task.contact_id is None:
      current_app.logger.info("Trigger: Contact attribute is not set")
      continue 
    contact = db.session.query(Person).filter(Person.id == task.contact_id).first()
    if contact is None:
      current_app.logger.info("Trigger: Unable to find Contact")
      continue 
    recipients = [contact]
    notif_pri = PRI_TASKS_DUE
    prepare_notification(task, notif_type, notif_pri, subject, content, contact, recipients)

def handle_workflow_cycle_status_change(status):
  if status not in ['Completed', 'Verified']:
    return
  workflow_cycles= db.session.query(models.Cycle).filter(models.Cycle.status == status).all()
  for cycle in workflow_cycles:
    if cycle_obj.contact_id is None:
      current_app.logger.warn("Trigger: Cycle Contact attribute is not set")
      continue
    cycle_contact = db.session.query(Person).filter(Person.id == cycle_obj.contact_id).first()
    if cycle_contact is None:
      current_app.logger.warn("Trigger: Unable to find Cycle Contact")
      continue
    workflow_obj=db.session.query(models.Workflow).filter(models.Workflow.id == cycle.workflow_id).first()
    if workflow_obj is None:
      current_app.logger.warn("Trigger: Unable to find workflow")
      continue
    if status == 'Verified':
       new_status = 'Closed'
    else:
       new_status = 'Verified'
    #ToDo(Mouli): Check all cycle tasks are in status, then notify that tasks need to be changed 
    for person in workflow_obj.people:
      subject="Workflow Cycle " + '"' + cycle.title + '" ' + "is ready to be "  + new_status
      content="Workflow " + workflow_obj.title + " : " + request.url_root + workflow_obj._inflector.table_plural + \
        "/" + str(workflow_obj.id) + " due on " + str(workflow_obj.end_date)
      notif_type = 'Email_Digest'
      recipients.append(person)
      if len(recipients):
        prepare_notification(task, notif_type, notif_pri, subject, content, cycle_contact, recipients)

def handle_workflow_cycle_started(num_days):
  workflow_cycles= db.session.query(models.Cycle).all()
  for cycle in workflow_cycles:
    workflow_obj=db.session.query(models.Workflow).filter(models.Workflow.id == cycle.workflow_id).first()
    if workflow_obj is None:
      current_app.logger.warn("Trigger: Unable to find workflow")
      continue
    if cycle.contact_id is None:
      current_app.logger.warn("Trigger: Cycle Contact attribute is not set")
      continue
    cycle_contact = db.session.query(Person).filter(Person.id == cycle.contact_id).first()
    if cycle_contact is None: 
      current_app.logger.warn("Trigger: Unable to find contact for Cycle")
      continue
    if cycle.end_date != None and cycle.status != 'Started' and \
      (cycle.start_date - date.today()) == timedelta(num_days):
      subject="Workflow Cycle " + '"' + cycle.title + '" ' + "will start in " + str(num_days) + " days"
      content="Workflow: "  + workflow_obj.title + " URL: " + request.url_root + workflow_obj._inflector.table_plural + \
          "/" + str(workflow_obj.id) + " due on " + str(cycle.end_date)
      notif_type = 'Email_Digest'
      notif_pri = PRI_OTHERS
      recipients=[]
      for person in workflow_obj.people:
        recipients.append(person)
      if len(recipients):
        prepare_notification(cycle, notif_type, notif_pri, subject, content, cycle_contact, recipients)

#ToDo(Mouli) uncomment the PUT trigger after edit modal is completed
#@Resource.model_put.connect_via(models.CycleTaskGroupObjectTask)
def handle_task_put(sender, obj=None, src=None, service=None):
  current_app.logger.info("Trigger: Task status changed to " + src.status) 
  if not getattr(obj, 'status'): 
    current_app.logger.warn("Trigger: Status attribute is not modified")
    return
  notif_pri=PRI_TASK_CHANGES
  if src.contact_id is None:
    current_app.logger.warn("Trigger: Task Contact attribute is not set")
    return
  contact = db.session.query(Person).filter(Person.id == src.contact_id).first()
  if contact is None:
    current_app.logger.warn("Trigger: Unable to find Task Contact")
    return
  subject="Task " + '"' + src.title + '" ' + " status changed to " + src.status
  content="Task " + '"' + src.title + '" ' + "URL: " + request.url_root + \
    "/" + models.Task.__tablename__ + "/" + str(obj.task_group_task_id) + " due on " + str(src.end_date) + \
    " Contact: " + contact.name
  cycle_obj = get_cycle_for_task(src.cycle_task_group_object_id)
  if cycle_obj is None:
    current_app.logger.warn("Unable to find workflow cycle for task: " + src.title)
    return
  if cycle_obj.contact_id is None:
    current_app.logger.warn("Trigger: Cycle Contact attribute is not set")
    return
  cycle_contact = db.session.query(Person).filter(Person.id == cycle_obj.contact_id).first()
  if cycle_contact is None:
    current_app.logger.warn("Trigger: Unable to find Cycle Contact")
    return
  if obj.status in ['InProgress', 'Declined', 'Verified']: 
    notif_type='Email_Now'
    recipients = [contact]
    prepare_notification(src, notif_type, notif_pri, subject, content, cycle_contact, recipients)
    if obj.status in ['Verified']: 
      notif_type='Email_Digest'
      prepare_notification(src, notif_type, notif_pri, subject, content, cycle_contact, recipients)
  if obj.status in ['Completed']: 
    notif_type='Email_Digest'
    recipients=[cycle_contact]
    prepare_notification(src, notif_type, notif_pri, subject, content, contact, recipients)

def prepare_notification(src, notif_type, notif_pri, subject, content, owner, recipients, override=False):
  if notif_type == 'Email_Digest':
    emaildigest_notification = EmailDigestNotification()
    emaildigest_notification.notif_pri = notif_pri
    current_app.logger.info("preparing Email Digest")
    emaildigest_notification.prepare([src], owner, recipients, subject, content)
  elif notif_type == 'Email_Now':
    email_notification = EmailNotification()
    email_notification.notif_pri = notif_pri
    notification = email_notification.prepare([src], owner, recipients, subject, content)
    current_app.logger.info("Sending Email")
    email_notification.notify_one(notification)
  else:
    return None
  if override is True and notif_type != 'Email_Now':
    email_notification = EmailNotification()
    email_notification.notif_pri = notif_pri
    notification = email_notification.prepare([src], owner, recipients, subject, content)
    current_app.logger.info("Sending Email")
    email_notification.notify_one(notification)
