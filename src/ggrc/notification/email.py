# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


"""
 GGRC email notification module hook to prepares email, email digest, notify email to recipients
"""


from flask import current_app
from google.appengine.api import mail
from ggrc.models import Person, NotificationConfig
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


