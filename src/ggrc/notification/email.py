# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


"""
 GGRC email notification module hook to prepares email, email digest, notify email to recipients 
"""


from google.appengine.api import mail
from ggrc.models import Person, NotificationConfig, Notification, NotificationObject, NotificationRecipient
from datetime import datetime
from ggrc import db


def isNotificationEnabled(person_id, notif_type):
  notification_config = NotificationConfig.query.\
    filter(NotificationConfig.person_id==person_id).\
    filter(NotificationConfig.notif_type==notif_type).\
    first()
  if notification_config is None:
    if notif_type == 'Email_Digest':
      return True
    else:
      return False
  else:
    return notification_config.enable_flag
  
class NotificationBase(object):
  notif_type = None
  notif_pri = None

  def __init__(self, notif_type):
    self.notif_type = notif_type

  def prepare(self, target_objs, sender, recipients, subject, content):
    return None

  def notify(self):
    pass

  def notify_one(self, notification):
    pass


class EmailNotification(NotificationBase):
  def __init__(self, notif_type='Email_Now'):
    super(EmailNotification, self).__init__(notif_type)

  def prepare(self, target_objs, sender, recipients, subject, content):
    now = datetime.now()
    notification = Notification(
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
        status='InProgress',
        notif_type=self.notif_type,
        recipient_id=recipient.id,
        notification=notification
      )
      db.session.add(notification_recipient)
      db.session.flush()

    return notification

  def notify(self):
    pending_notifications = db.session.query(Notification).\
      join(Notification.recipients).\
      filter(NotificationRecipient.status == 'InProgress').\
      filter(NotificationRecipient.notif_type == self.notif_type)

    enable_notif={}
    for notification in pending_notifications:
      sender = Person.query.filter(Person.id==notification.sender_id).first()
      assignees = {}
      for notify_recipient in notification.recipients:
        if notify_recipient.notif_type != self.notif_type:
          continue
        recipient_id=notify_recipient.recipient_id
        if recipient_id is None:
          continue
        if not enable_notif.has_key(recipient_id):
          enable_notif[recipient_id]=isNotificationEnabled(recipient_id, self.notif_type)
        if not enable_notif[recipient_id]:
          continue
        recipient = Person.query.filter(Person.id==recipient_id).first()
        if recipient is None:
          continue
        if not assignees.has_key(recipient.id):
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
        if notify_recipient.notif_type != self.notif_type:
          continue
        if enable_notif.has_key(notify_recipient.recipient_id) and \
           enable_notif[notify_recipient.recipient_id]:
          notify_recipient.status="Successful"
        else:
          notify_recipient.status="NotificationDisabled"
        db.session.add(notify_recipient)
        db.session.flush()

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
      if not enable_notif.has_key(recipient_id):
        if override:
          enable_notif[recipient_id]=True
        else:
          enable_notif[recipient_id]=isNotificationEnabled(recipient_id, self.notif_type)
      if not enable_notif[recipient_id]:
        continue
      recipient=Person.query.filter(Person.id==recipient_id).first()
      if recipient is None:
        continue
      if not assignees.has_key(recipient.id):
        assignees[recipient.id] = recipient.name + " <" + recipient.email + ">"

    if len(assignees) < 1:
      return

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

    for notify_recipient in notification.recipients:
      if notify_recipient.notif_type != self.notif_type:
        continue
      if enable_notif.has_key(notify_recipient.recipient_id) and \
         enable_notif[notify_recipient.recipient_id]:
        notify_recipient.status="Successful"
      else:
        notify_recipient.status="NotificationDisabled"
      db.session.add(notify_recipient)
      db.session.flush()

class EmailDigestNotification(EmailNotification):
  def __init__(self, notif_type='Email_Digest'):
    super(EmailDigestNotification, self).__init__(notif_type)

  def notify(self):
    pending_notifications = db.session.query(Notification).\
      join(Notification.recipients).\
      filter(NotificationRecipient.status == 'InProgress').\
      filter(NotificationRecipient.notif_type == self.notif_type)

    pending_notifications_by_date = {}
    for notification in pending_notifications:
      notif_date = notification.notif_date.strftime('%Y/%m/%d')
      if not pending_notifications_by_date.has_key(notif_date):
        pending_notifications_by_date[notif_date]=[]
      pending_notifications_by_date[notif_date].append(notification)

    to={}
    sender_ids={}
    enable_notif={}
    for notif_date, notifications in pending_notifications_by_date.items():
      content={}
      subject="gGRC daily email digest for " + notif_date
      empty_line = """

      """
      for notification in notifications:
        sender_id = notification.sender_id
        notif_pri = notification.notif_pri
        if not sender_ids.has_key(sender_id):
          sender = Person.query.filter(Person.id==sender_id).first()
          if sender is None:
            continue
          sender_ids[sender_id] = sender

        for notify_recipient in notification.recipients:
          if notify_recipient.notif_type != self.notif_type:
            continue
          recipient_id=notify_recipient.recipient_id
          if recipient_id is None:
            continue
          if not enable_notif.has_key(recipient_id):
            enable_notif[recipient_id] = isNotificationEnabled(recipient_id, self.notif_type)
          if not enable_notif[recipient_id]:
            continue
          if not to.has_key(recipient_id):
            recipient = Person.query.filter(Person.id==recipient_id).first()
            if recipient is None:
              continue
            to[recipient_id]=recipient
          key=(recipient_id, sender_id)
          if not content.has_key(key):
            content[key]={}
          if not content[key].has_key(notification.notif_pri):
            content[key][notif_pri]=""
          content[key][notif_pri] = content[key][notif_pri] + empty_line + notification.content

      for (recipient_id, sender_id), items in content.items():
        recipient=to[recipient_id] 
        sender=sender_ids[sender_id] 
        import collections
        sorted_items = collections.OrderedDict(sorted(items.items()))
        body=""
        for key, value in sorted_items.items():
          body = body + value
        message = mail.EmailMessage(
          sender=sender.name + "<" + sender.email + ">", 
          to=recipient.name + "<" + recipient.email + ">", 
          subject=subject,
          body=body)
        message.send()

      for notification in notifications:
        for notify_recipient in notification.recipients:
          if notify_recipient.notif_type != self.notif_type:
            continue
          if enable_notif.has_key(notify_recipient.recipient_id) and \
             enable_notif[notify_recipient.recipient_id]:
            notify_recipient.status="Successful"
          else:
            notify_recipient.status="NotificationDisabled"
          db.session.add(notify_recipient)
          db.session.flush()
