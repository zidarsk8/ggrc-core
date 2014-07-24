# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


"""
 GGRC email notification module hook to prepares email, email digest, notify email to recipients 
"""


from flask import current_app
from google.appengine.api import mail
from ggrc.models import Person, NotificationConfig, Notification, NotificationObject, NotificationRecipient
from datetime import datetime, timedelta
from ggrc import db
from ggrc import settings


def getAppEngineEmail():
  appengine_email = getattr(settings, 'APPENGINE_EMAIL') 
  if appengine_email is not None and appengine_email != '' and appengine_email !=" ":
    return appengine_email
  else:
    return None
   
def isNotificationEnabled(person_id, notif_type):
  if notif_type == 'Email_Deferred':
    notif_type='Email_Now'
  elif notif_type == 'Email_Digest_Deferred':
    notif_type='Email_Digest'
  notification_config=NotificationConfig.query.\
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
  notif_type=None
  notif_pri=None
  appengine_email=None

  def __init__(self, notif_type):
    self.notif_type=notif_type
    self.appengine_email = getAppEngineEmail()

  def prepare(self, target_objs, sender, recipients, subject, content, override):
    return None

  def notify(self):
    pass

  def notify_one(self, notification, notify_custom_message):
    pass


class EmailNotification(NotificationBase):
  def __init__(self, notif_type='Email_Now'):
    super(EmailNotification, self).__init__(notif_type)

  def get_ignored_notifications(self, notifs):
    ignored_notifs={}
    #ToDo(Mouli): The valid states mapping must be set outside the generic email notification module
    ignored_states={
      'CycleTaskGroupObjectTask': ['Finished'],
      'CycleTaskGroup': ['InProgress', 'Verified'],
    }
    for notif in notifs:
      for notif_object in notif.notification_object:
        if ignored_states.has_key(notif_object.object_type):
          states=ignored_states[notif_object.object_type]
          if notif_object.status in states:
            ignored_notifs[notif.id]=notif

    return ignored_notifs

  def get_skipped_notifications(self, notifs_by_target):
    skipped_notifs={}
    #ToDo(Mouli): The valid states mapping must be set outside the generic email notification module
    valid_states={
      'CycleTaskGroupObjectTask': ['Assigned', 'InProgress', 'Finished', 'Verified', 'Declined'],
      'CycleTaskGroup': ['InProgress', 'Finished', 'Verified'],
    }
    valid_transition_task={
     'Assigned': 'InProgress',
     'InProgress': 'Finished',
     'Finished': 'Declined',
     'Finished': 'Verified',
    }
    valid_transition_taskgroup={
     'InProgress': 'Finished',
     'Finished': 'Verified',
    }
    valid_transition={
      'CycleTaskGroupObjectTask': valid_transition_task,
      'CycleTaskGroup': valid_transition_taskgroup,
    }
    undo_transition_task={
     'InProgress': 'Assigned',
     'Finished': 'InProgress',
     'Declined':'Finished',
     'Verified': 'Finished',
    }
    undo_transition_taskgroup={
     'Finished': 'InProgress',
     'Verified': 'Finished',
    }
    undo_transition={
      'CycleTaskGroupObjectTask': undo_transition_task,
      'CycleTaskGroup': undo_transition_taskgroup,
    }
    for key, target_notifs in notifs_by_target.items():
      type=key[0]
      cnt = 0
      if not valid_states.has_key(type):
        current_app.logger.error("EmailDeferredNotification: Error occured in handling state transitions")
        for notif in target_notifs:
          skipped_notifs[notif.id]=notif
        continue

      for valid_state in valid_states[type]:
        next_cnt=find_matching_entry(target_notifs, cnt, valid_state, valid_state)
        if cnt != next_cnt:
          for index_cnt in range(next_cnt-cnt):
            notif=target_notifs[cnt+index_cnt][0]
            skipped_notifs[notif.id]=notif
        cnt=next_cnt
        if undo_transition[type].has_key(valid_state):
          next_cnt=find_matching_entry(target_notifs, cnt, valid_state, undo_transition[type][valid_state])
          if cnt != next_cnt:
            for index_cnt in range(next_cnt-cnt):
              notif=target_notifs[cnt+index_cnt][0]
              skipped_notifs[notif.id]=notif
        cnt=next_cnt
        if valid_transition[type].has_key(valid_state):
          cnt=find_matching_entry(target_notifs, cnt, valid_state, valid_transition[type][valid_state])
    return skipped_notifs

  def prepare(self, target_objs, sender, recipients, subject, content, override=False):
    if self.appengine_email is None:
      return None
    enable_notif={}
    existing_recipients={}
    updated_recipients=[]
    for recipient in recipients:
      recipient_id=recipient.id
      existing_recipients[recipient.id]=recipient
      if recipient_id is None:
        continue
      if not enable_notif.has_key(recipient_id):
        if override:
          enable_notif[recipient_id]=True
        else:
          enable_notif[recipient_id]=isNotificationEnabled(recipient_id, self.notif_type)
    if len(enable_notif) > 0:
      for id, enable_flag in enable_notif.items():
        if enable_flag:
          updated_recipients.append(existing_recipients[id])
    else:
      current_app.logger.info("EmailNotification: recipient list is empty")
      return None
    if not len(updated_recipients) > 0:
      current_app.logger.info("EmailNotification: No recipients found with notification enabled")
      return None
     
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

    for recipient in updated_recipients:
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

    for notification in pending_notifications:
      self.notify_one(notification)

  def notify_one(self, notification, notify_custom_message=None):
    sender=Person.query.filter(Person.id==notification.sender_id).first()
    assignees={}
    assignees_with_custom_message={}
    notif_error={}
    for notify_recipient in notification.recipients:
      if notify_recipient.notif_type != self.notif_type:
        continue
      recipient_id=notify_recipient.recipient_id
      if recipient_id is None:
        continue
      recipient=Person.query.filter(Person.id==recipient_id).first()
      if recipient is None:
        continue
      if notify_custom_message is not None and notify_custom_message.has_key(recipient.id):
        if not assignees_with_custom_message.has_key(recipient.id):
          assignees_with_custom_message[recipient.id]=recipient.name + " <" + recipient.email + ">"
      else:
        if not assignees.has_key(recipient.id):
          assignees[recipient.id]=recipient.name + " <" + recipient.email + ">"

    if len(assignees) > 0:
      to_list=""
      cnt=0
      for id, assignee in assignees.items():
        to_list=to_list + assignee
        if cnt < len(assignees)-1:
          to_list=to_list + ","
        cnt=cnt+1
      sender_info=sender.name + "<" + sender.email + ">" 
      email_headers={"On-Behalf-Of":sender_info}
      message=mail.EmailMessage(
        sender="gGRC Administrator on behalf of " + sender.name +  "<" + self.appengine_email + ">",
        to=to_list,
        subject=notification.subject,
        headers=email_headers,
        html=notification.content,
        body=notification.content)
      try:
        message.send()
      except: 
        notif_error[id]="Unable to send email to " + to_list
        current_app.logger.error("Unable to send email to " + to_list) 

    empty_line="""
    """
    for id, assignee in assignees_with_custom_message.items():
      message=mail.EmailMessage(
        sender="gGRC Administrator on behalf of " + sender.name +  "<" + self.appengine_email + ">",
        to=assignee,
        subject=notification.subject,
        headers=email_headers,
        html=notify_custom_message[id] + empty_line +  notification.content,
        body=notify_custom_message[id] + empty_line +  notification.content)

      try:
        message.send()
      except: 
        notif_error[id]="Unable to send email to " + assignee
        current_app.logger.error("Unable to send email to " + assignee) 

    for notify_recipient in notification.recipients:
      if notify_recipient.notif_type != self.notif_type:
        continue
      if not notif_error.has_key(notify_recipient.recipient_id):
        notify_recipient.status="Successful"
      else:
        notify_recipient.status="Failed"
        notify_recipient.error_text=notif_error[notify_recipient.recipient_id]
      db.session.add(notify_recipient)
      db.session.flush()

class EmailDigestNotification(EmailNotification):
  def __init__(self, notif_type='Email_Digest'):
    super(EmailDigestNotification, self).__init__(notif_type)

  def notify(self):
    pending_notifications=db.session.query(Notification).\
      join(Notification.recipients).\
      filter(NotificationRecipient.status == 'InProgress').\
      filter(NotificationRecipient.notif_type == self.notif_type)
    self.notify_pending(pending_notifications)

  def notify_pending(self, pending_notifications):
    pending_notifications_by_date={}
    for notification in pending_notifications:
      notif_date=notification.notif_date.strftime('%Y/%m/%d')
      if not pending_notifications_by_date.has_key(notif_date):
        pending_notifications_by_date[notif_date]=[]
      pending_notifications_by_date[notif_date].append(notification)

    to={}
    sender_ids={}
    notif_error={}
    for notif_date, notifications in pending_notifications_by_date.items():
      content={}
      content_for_recipients={}
      begin_message={}
      subject="gGRC daily email digest for " + notif_date
      empty_line = """
      """
      empty_line2 = """

      """
      for notification in notifications:
        sender_id=notification.sender_id
        notif_pri=notification.notif_pri
        if not sender_ids.has_key(sender_id):
          sender=Person.query.filter(Person.id==sender_id).first()
          if sender is None:
            continue
          sender_ids[sender_id]=sender
        for notify_recipient in notification.recipients:
          if notify_recipient.notif_type != self.notif_type:
            continue
          recipient_id=notify_recipient.recipient_id
          if recipient_id is None:
            continue
          if not to.has_key(recipient_id):
            recipient=Person.query.filter(Person.id==recipient_id).first()
            if recipient is None:
              continue
            to[recipient_id]=recipient
          key=(recipient_id, sender_id)
          if not content.has_key(key):
            content[key]={}
          if not content[key].has_key(notification.notif_pri):
            content[key][notif_pri]=""
          content[key][notif_pri]=content[key][notif_pri] + empty_line + notification.content

      for (recipient_id, sender_id), items in content.items():
        recipient=to[recipient_id] 
        sender=sender_ids[sender_id] 
        import collections
        sorted_items=collections.OrderedDict(sorted(items.items()))
        body=""
        for key, value in sorted_items.items():
          body=body + value
        if not content_for_recipients.has_key(recipient_id):
          content_for_recipients[recipient_id]= ""
        if not begin_message.has_key((recipient_id, sender_id)):
          begin_message[(recipient_id, sender_id)] = empty_line2 +\
            "Emails sent by " + sender.name 
          content_for_recipients[recipient_id]= content_for_recipients[recipient_id] + \
            begin_message[(recipient_id, sender_id)]
        content_for_recipients[recipient_id]= content_for_recipients[recipient_id] + body
      
      for recipient_id, body in content_for_recipients.items():
        recipient=to[recipient_id] 
        message=mail.EmailMessage(
          sender="gGRC Administrator" + "<" + self.appengine_email + ">",
          to=recipient.name + "<" + recipient.email + ">", 
          subject=subject,
          body=body)
        try:
          message.send()
        except:
          notif_error[id]="Unable to send email to " + recipient.name
          current_app.logger.error("Unable to send email to " + recipient.name)

      for notification in notifications:
        for notify_recipient in notification.recipients:
          if notify_recipient.notif_type != self.notif_type:
            continue
          if not notif_error.has_key(notify_recipient.recipient_id):
            notify_recipient.status="Successful"
          else:
            notify_recipient.status="Failed"
          db.session.add(notify_recipient)
        db.session.flush()

class EmailDeferredNotification(EmailNotification):
  def __init__(self, notif_type='Email_Deferred'):
    super(EmailDeferredNotification, self).__init__(notif_type)

  def notify(self):
    deferred_notifs=db.session.query(Notification).\
      join(Notification.recipients).\
      filter(Notification.notif_date < (datetime.now() - timedelta(minutes=60))).\
      filter(NotificationRecipient.status == 'InProgress').\
      filter(NotificationRecipient.notif_type == self.notif_type)
    notifs_by_target={}
    for notification in deferred_notifs: 
      for notify_recipient in notification.recipients:
        user_id=notify_recipient.id
        break
      for notif_object in notification.notification_object:
        object_id=notif_object.object_id
        object_type=notif_object.object_type
        if not notifs_by_target.has_key(object_id):
          notifs_by_target[(object_type, object_id, user_id)]=[]
        notifs_by_target[(object_type, object_id, user_id)].append((notification, notif_object))
    skipped_notifs=self.get_skipped_notifications(notifs_by_target)
    ignored_notifs=self.get_ignored_notifications(deferred_notifs)
    for notif in deferred_notifs:
      if not skipped_notifs.has_key(notif.id) and not ignored_notifs.has_key(notif.id):
        self.notify_one(notif) 
    for id, notif in skipped_notifs.items():
      for notify_recipient in notif.recipients:
        if notify_recipient.notif_type != self.notif_type:
          continue
        notify_recipient.status="Skipped"
        db.session.add(notify_recipient)
        db.session.flush()
    for id, notif in ignored_notifs.items():
      for notify_recipient in notif.recipients:
        if notify_recipient.notif_type != self.notif_type:
          continue
        notify_recipient.status="Skipped"
        db.session.add(notify_recipient)
        db.session.flush()

class EmailDigestDeferredNotification(EmailDigestNotification):
  def __init__(self, notif_type='Email_Digest_Deferred'):
    super(EmailDigestDeferredNotification, self).__init__(notif_type)

  def notify(self):
    deferred_notifs=db.session.query(Notification).\
      join(Notification.recipients).\
      filter(Notification.notif_date < (datetime.now() - timedelta(minutes=60))).\
      filter(NotificationRecipient.status == 'InProgress').\
      filter(NotificationRecipient.notif_type == self.notif_type)
    notifs_by_target={}
    for notification in deferred_notifs: 
      # ToDO(Mouli): The design supports only 1 recipient for notification object for handling deferred notification 
      for notify_recipient in notification.recipients:
        user_id=notify_recipient.id
        break
      for notif_object in notification.notification_object:
        object_id=notif_object.object_id
        object_type=notif_object.object_type
        if not notifs_by_target.has_key(object_id):
          notifs_by_target[(object_type, object_id, user_id)]=[]
        notifs_by_target[(object_type, object_id, user_id)].append((notification, notif_object))
    skipped_notifs=self.get_skipped_notifications(notifs_by_target)
    ignored_notifs=self.get_ignored_notifications(deferred_notifs)
    emaildigest_notif=[]
    for notif in deferred_notifs:
      if not skipped_notifs.has_key(notif.id) and not ignored_notifs.has_key(notif.id):
        emaildigest_notif.append(notif)
    if len(emaildigest_notif) > 0:
      for notif in emaildigest_notif:
        for notify_recipient in notif.recipients:
          if notify_recipient.notif_type != self.notif_type:
            continue
          notify_recipient.notif_type="Email_Digest"
          db.session.add(notify_recipient)
          db.session.flush()
    for id, notif in skipped_notifs.items():
      for notify_recipient in notif.recipients:
        if notify_recipient.notif_type != self.notif_type:
          continue
        notify_recipient.status="Skipped"
        db.session.add(notify_recipient)
        db.session.flush()
    for id, notif in ignored_notifs.items():
      for notify_recipient in notif.recipients:
        if notify_recipient.notif_type != self.notif_type:
          continue
        notify_recipient.status="Skipped"
        db.session.add(notify_recipient)
        db.session.flush()

def find_matching_entry(notif_objects, start, start_state, end_state):
  if notif_objects[start][1].status != start_state:
    return start
  cnt=start
  matching_cnt=cnt
  while cnt < len(notif_objects):
    if notif_objects[cnt][1].status == end_state:
      matching_cnt=cnt
    cnt=cnt+1
  return matching_cnt
