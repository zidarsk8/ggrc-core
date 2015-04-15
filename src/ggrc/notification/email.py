# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


"""
 GGRC email notification module hook to prepares email, email digest, notify
 email to recipients
"""


from google.appengine.api import mail
from ggrc import settings


def getAppEngineEmail():
  email = getattr(settings, 'APPENGINE_EMAIL')
  if email is not None and email != '' and email != " ":
    return email
  else:
    return None


def send_email(user_email, subject, body):
  sender = getAppEngineEmail()
  if mail.is_email_valid(user_email) and mail.is_email_valid(sender):
    message = mail.EmailMessage(sender=sender, subject=subject)

    message.to = user_email
    message.body = "TODO: add email in text mode."
    message.html = body

    message.send()
