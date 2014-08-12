# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


"""
 GGRC calendar service base class
"""


from flask import current_app
from werkzeug.exceptions import Forbidden
from ggrc.notification import NotificationBase, isNotificationEnabled
from ggrc.models import Person, Notification, NotificationObject, NotificationRecipient
from ggrc.models import CalendarEntry
from datetime import datetime
from ggrc import db
from ggrc import settings

GGRC_CALENDAR='GGRC Calendar'

class CalendarNotification(NotificationBase):
  start_date=None
  end_date=None
  calendar_service=None
  calendar_event=None
  calendar=None
  owner_id=None
  enable_flag=None
  def __init__(self, notif_type='Calendar'):
    super(CalendarNotification, self).__init__(notif_type)

  def prepare(self, target_objs, sender, recipients, subject, content):
    now=datetime.now()
    notification=Notification(
      notif_pri=self.notif_pri,
      notif_date=now,
      created_at=now,
      content=content,
      subject=subject,
      sender_id=sender.id
     )
    db.session.add(notification)
    db.session.flush()

    for obj in target_objs:
      if hasattr(obj, 'status'):
        status=obj.status
      else:
        status='InProgress'
      notification_object=NotificationObject(
        created_at=datetime.now(),
        object_id=obj.id,
        object_type=obj.type,
        modified_by_id=sender.id,
        status=status,
        notification=notification
      )
      db.session.add(notification_object)
      db.session.flush()

    for recipient in recipients:
      notification_recipient=NotificationRecipient(
        created_at=datetime.now(),
        status='InProgress',
        notif_type=self.notif_type,
        recipient_id=recipient.id,
        notification=notification
      )
      db.session.add(notification_recipient)
      db.session.flush()

    return notification

  def notify(self):
    pending_notifications=db.session.query(Notification).\
      join(Notification.recipients).\
      filter(NotificationRecipient.status == 'InProgress').\
      filter(NotificationRecipient.notif_type == self.notif_type)

    enable_notif={}
    for notification in pending_notifications:
      self.notify_one(notification)

  def notify_one(self, notification, override=False):
    sender=Person.query.filter(Person.id==notification.sender_id).first()
    assignees={}
    enable_notif={}
    for notify_recipient in notification.recipients:
      if notify_recipient.notif_type != self.notif_type:
        continue
      recipient_id=notify_recipient.recipient_id
      if recipient_id is None:
        continue
      if self.enable_flag and self.enable_flag.has_key(recipient_id):
        enable_notif[recipient_id]=self.enable_flag[recipient_id]
      else:
        if not enable_notif.has_key(recipient_id):
          if override:
            enable_notif[recipient_id]=True
          else:
            enable_notif[recipient_id]=isNotificationEnabled(recipient_id, self.notif_type)
      recipient=Person.query.filter(Person.id==recipient_id).first()
      if recipient is None:
        continue
      if not assignees.has_key(recipient.id):
        assignees[recipient.id]={'email': recipient.email}

    event_details= {
      'summary': notification.subject,
      'start': {
        'date': str(self.start_date)
      },
      'end': {
        'date': str(self.end_date)
      },
      'description':  notification.content,
      'anyoneCanAddSelf': True,
      'reminders': {
         'useDefault': False,
         'overrides': [
            {
              'method': 'popup',
              'minutes': 4320,
            },
            {
              'method': 'popup',
              'minutes': 1440,
            },
         ]
       }
    }
    notify_error=False
    calendar_event=self.calendar_event
    calendar=self.calendar
    if len(assignees)> 0:
      if calendar_event is None:
        calendar_event =create_calendar_event(
          self.calendar_service, 
          calendar['id'], 
          event_details)
        if calendar_event is None:
          notify_error=True
          notify_error_text="Error occured in creating calendar event, id: " +\
            sender.email + " event: " + event_details['summary']
          current_app.logger.error(notify_error_text)
      if calendar_event is not None: 
        calendar_event['attendees']=[]
        for id, assignee in assignees.items():
          recipient_email=assignee['email']
          if enable_notif.has_key(id) and enable_notif[id]:
            calendar_event['attendees'].append(assignee)
          else:
            continue
        updated_event=update_calendar_event(
          self.calendar_service, 
          calendar['id'], 
          calendar_event['id'], 
          calendar_event)
        if updated_event is None:
          notify_error=True
          notify_error_text="Error occured in updating calendar: " + \
            sender.email + " for event: " + calendar_event['summary']
          current_app.logger.error(notify_error_text)

    for notify_recipient in notification.recipients:
      if notify_recipient.notif_type != self.notif_type:
        continue
      if notify_error:
        notify_recipient.status="Failed"
        notify_recipient.error_text=notify_error_text
      elif enable_notif.has_key(notify_recipient.recipient_id) and \
         enable_notif[notify_recipient.recipient_id]:
        notify_recipient.status="Successful"
      else:
        notify_recipient.status="NotificationDisabled"
      db.session.add(notify_recipient)
      db.session.flush()

class CalendarService(object):
  calendar_service=None
  credentials=None

  def __init__(self, credentials=None):
    if credentials is not None:
      self.credentials=credentials
      from apiclient.discovery import build
      import httplib2
      http = httplib2.Http()
      http = self.credentials.authorize(http)
      self.calendar_service=build(serviceName='calendar', version='v3', http=http)

def create_calendar_entry(calendar_service, calendar_name, owner_id):
  from apiclient import errors
  calendar=None
  calendar_object=None
  calendar_entry = {
    'summary': calendar_name
  }
  try:
    calendar=calendar_service.calendars().insert(
      body=calendar_entry).execute()
  except errors.HttpError, error:
    current_app.logger.error("HTTP Error occured in creating calendar with ID: " + calendar_name + " " +  str(error))
    raise Forbidden()
  except Exception, error:
    current_app.logger.error("Exception occured in creating calendar with ID: " + calendar_name + " " +  str(error))
    raise Forbidden()
  if calendar is not None:
    calendar_object=CalendarEntry(
      owner_id=owner_id,
      name=calendar_name,
      calendar_id=calendar['id'])
    db.session.add(calendar_object)
    db.session.flush()
  return calendar

def get_calendar(calendar_service, calendar_id):
  from apiclient import errors
  try:
    calendar=calendar_service.calendars().get(calendarId=calendar_id).execute()
  except errors.HttpError, error:
    current_app.logger.error("HTTP Error occured in getting calendar for ID: " + calendar_id + " " +  str(error))
    raise Forbidden()
  except Exception, error:
    current_app.logger.error("Exception occured in getting calendar for ID: " + calendar_id + " " +  str(error))
    raise Forbidden()
  return calendar

def find_calendar_entry(calendar_service, calendar_name, owner_id):
  calendar=None
  calendar_entries=db.session.query(CalendarEntry).\
    filter(CalendarEntry.name== calendar_name).\
    filter(CalendarEntry.owner_id == owner_id).all()
  for calendar_entry in calendar_entries:
   calendar=get_calendar(calendar_service, calendar_entry.calendar_id)
   if calendar is not None:
     break
  return calendar

def create_calendar_event(calendar_service, calendar_id, event_details):
  from apiclient import errors
  calendar_event=None
  try:
    calendar_event=calendar_service.events().insert(
      calendarId=calendar_id,
      body=event_details).execute()
  except errors.HttpError, error:
    current_app.logger.error("HTTP Error occured in creating calendar event: " + str(error))
    raise Forbidden()
  except Exception, error:
    current_app.logger.error("Exception occured in creating calendar event: " + str(error))
    raise Forbidden()
  return calendar_event

def delete_calendar_event(calendar_service, calendar_id, event_id):
  from apiclient import errors
  calendar_event=None
  try:
    calendar_service.events().delete(
      calendarId=calendar_id,
      eventId=event_id).execute()
  except errors.HttpError, error:
    current_app.logger.error("Exception occured in deleting calendar event: " + str(error))
    raise Forbidden()
  except Exception, error:
    current_app.logger.error("Exception occured in deleting calendar event: " + str(error))
    raise Forbidden()
  return 

def get_calendar_event(calendar_service, calendar_id, event_id):
  from apiclient import errors
  page_token = None
  while True:
    try:
      events=calendar_service.events().list(calendarId=calendar_id, q=event_id, pageToken=page_token).execute()
    except errors.HttpError, error:
      current_app.logger.error("HTTP Error occured in getting calendar events: " + str(error))
      raise Forbidden()
    except Exception, error:
      current_app.logger.error("Exception occured in getting calendar events: " + str(error))
      raise Forbidden()
    for event in events['items']:
      if event.has_key('summary'):
        if event['summary'] in [event_id]:
          return event 
    page_token = events.get('nextPageToken')
    if not page_token:
      break
  return None

def update_calendar_event(calendar_service, calendar_id, event_id, event_details):
  from apiclient import errors
  calendar_event=None
  try:
    calendar_event=calendar_service.events().update(
      calendarId=calendar_id,
      eventId=event_id,
      body=event_details).execute()
  except errors.HttpError, error:
    current_app.logger.error("HTTP Error occured in updating calendar event: " + str(error))
    raise Forbidden()
  except Exception, error:
    current_app.logger.error("Exception occured in updating calendar event: " + str(error))
    raise Forbidden()
  return calendar_event 

def create_calendar_acl(calendar_service, calendar_id, recipient_email, role):
  from apiclient import errors
  calendar_acl=None
  rule={
    'scope': {
      'type': 'user',
      'value': recipient_email,
    },
    'role': role,
  }
  try:
    calendar_acl=calendar_service.acl().insert(
      calendarId=calendar_id,
      body=rule).execute()
  except errors.HttpError, error:
    current_app.logger.error("HTTP Error occured in creating calendar ACL: " + str(error))
    raise Forbidden()
  except Exception, error:
    current_app.logger.error("Exception occured in creating calendar ACL: " + str(error))
    raise Forbidden()
  return calendar_acl

def create_calendar_acls(calendar_service, calendar_id, assignee_emails, skip_emails, role):
   calendar_acls=[]
   for recipient_email in assignee_emails:
     if recipient_email in skip_emails:
       continue
     calendar_acl=get_calendar_acl(calendar_service, calendar_id, recipient_email, role)
     if calendar_acl is None:
       calendar_acl=create_calendar_acl(calendar_service, calendar_id, recipient_email, role)
       if calendar_acl is not None:
         calendar_acls.append(calendar_acl)
       else:
         return None
       calendar_acls.append(calendar_acl)
   return calendar_acls

def get_calendar_acl(calendar_service, calendar_id, recipient_email, role):
  from apiclient import errors
  page_token = None
  while True:
    try:
      acls=calendar_service.acl().list(calendarId=calendar_id, pageToken=page_token).execute()
    except errors.HttpError, error:
      current_app.logger.error("HTTP Error occured in getting calendar acl: " + str(error))
      raise Forbidden()
    except Exception, error:
      current_app.logger.error("Exception occured in getting calendar acl: " + str(error))
      raise Forbidden()
    for rule in acls['items']:
      if rule['role'] != role:
        continue
      if rule['scope']['type'] != 'user':
        continue
      if rule['scope']['value'] != recipient_email:
        continue
      else:
        return rule
    page_token = acls.get('nextPageToken')
    if not page_token:
      break
  return None
