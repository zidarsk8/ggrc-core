# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


"""
 GGRC email notification module prepares email, email digest, notify email to recipients when it is triggerd
"""


from google.appengine.api import mail
from ggrc.models import Person, NotificationConfig, Notification, NotificationObject, NotificationRecipient
from datetime import datetime
from ggrc import db


class NotificationBase(object):
  notif_type = None

  def __init__(self, notif_type):
    self.notif_type = notif_type

  def prepare(self, target_objs, sender, recipients, subject, content):
    pass

  def notify(self):
    pass


class EmailNotification(NotificationBase):
  def __init__(self, notif_type='Email_Now'):
    super(EmailNotification, self).__init__(notif_type)

  def prepare(self, target_objs, sender, recipients, subject, content):
    now = datetime.now()
    notification = Notification(
      notif_date=now,
      created_at=now,
      content=content,
      subject=subject,
      sender_id=sender.id
     )
    db.session.add(notification)
    db.session.flush()

    for obj in target_objs:
      notification_object = NotificationObject(
        created_at=datetime.now(),
        object_id=obj.id, 
        object_type=obj.type,
        notification=notification
      )
      db.session.add(notification_object)
      db.session.flush()

    for recipient in recipients:
      notification_recipient = NotificationRecipient(
        created_at=datetime.now(),
        status='Progress',
        notif_type=self.notif_type,
        recipient_id=recipient.id,
        notification=notification
      )
      db.session.add(notification_recipient)
      db.session.flush()

    db.session.commit()

  def notify(self):
    pending_notifications = db.session.query(Notification).\
      join(Notification.recipients).\
      filter(NotificationRecipient.status == 'Progress').\
      filter(NotificationRecipient.notif_type == self.notif_type)

    for notification in pending_notifications:
      sender = Person.query.filter(Person.id==notification.sender_id).first()
      assignees = {}
      for notify_recipient in notification.recipients:
        recipient = Person.query.filter(Person.id==notify_recipient.recipient_id).first()
        assignees[recipient.id] = recipient.name + " <" + recipient.email + ">"

      if len(assignees) < 1:
        continue 
      to_list = ""
      cnt = 0
      for id, assignee in assignees.items():
        to_list = to_list + assignee
        if cnt < len(assignees)-1:
          to_list + ","

      message = mail.EmailMessage(
        sender=sender.name + "<" + sender.email + ">", 
        to=to_list,
        subject=notification.subject,
        body=notification.content)
      message.send()

    for notification in pending_notifications:
      for notify_recipient in notification.recipients:
        notify_recipient.status="Successful"
        db.session.add(notify_recipient)
        db.session.flush()
    db.session.commit()


class EmailDigestNotification(EmailNotification):
  def __init__(self, notif_type='Email_Digest'):
    super(EmailDigestNotification, self).__init__(notif_type)

  def notify(self):
    pending_notifications = db.session.query(Notification).\
      join(Notification.recipients).\
      filter(NotificationRecipient.status == 'Progress').\
      filter(NotificationRecipient.notif_type == self.notif_type)

    pending_notifications_by_date = {}
    for notification in pending_notifications:
      notif_date = notification.notif_date.strftime('%Y/%m/%d')
      if not pending_notifications_by_date.has_key(notif_date):
        pending_notifications_by_date[notif_date]=[]
      pending_notifications_by_date[notif_date].append(notification)
  
    for notif_date, notifications in pending_notifications_by_date.items():
      empty_line = """

      """
      content = ""
      assignees = {}
      for notification in notifications:
        sender = Person.query.filter(Person.id==notification.sender_id).first()
        for notify_recipient in notification.recipients:
          recipient = Person.query.filter(Person.id==notify_recipient.recipient_id).first()
          assignees[recipient.id]=recipient
        if len(assignees) < 1:
          continue
        content = content + empty_line + notification.content
        subject = notification.subject

      if len(assignees) < 1:
        return
      to_list = ""
      cnt = 0
      for id, assignee in assignees.items():
        to_list = to_list + assignee.name + " <" + assignee.email + ">"
        if cnt < len(assignees)-1:
          to_list = to_list + ', '
         
      message = mail.EmailMessage(
        sender=sender.name + "<" + sender.email + ">", 
        to=to_list,
        subject=subject,
        body=content)
      message.send()

      for notification in notifications:
        for notify_recipient in notification.recipients:
          notify_recipient.status="Successful"
          db.session.add(notify_recipient)
          db.session.flush()
      db.session.commit()
