# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


"""
 GGRC email notification module hook to prepares email, email digest, notify
 email to recipients
"""


from google.appengine.api import mail
from ggrc.models import NotificationConfig
from ggrc import settings


def getAppEngineEmail():
  email = getattr(settings, 'APPENGINE_EMAIL')
  if email is not None and email != '' and email != " ":
    return email
  else:
    return None


def isNotificationEnabled(person_id, notif_type):
  if notif_type == 'Email_Deferred':
    notif_type = 'Email_Now'
  elif notif_type == 'Email_Digest_Deferred':
    notif_type = 'Email_Digest'
    notification_config = NotificationConfig.query.\
        filter(NotificationConfig.person_id == person_id).\
        filter(NotificationConfig.notif_type == notif_type).\
        first()
  if notification_config is None:
    if notif_type == 'Email_Digest':
      return True
    else:
      return False
  else:
    return notification_config.enable_flag


def send_email(user_email, subject, body):
  sender = getAppEngineEmail()
  if mail.is_email_valid(user_email) and mail.is_email_valid(sender):
    message = mail.EmailMessage(sender=sender, subject=subject)

    message.to = user_email
    message.body = "hello"
    message.html = body

    message.send()
