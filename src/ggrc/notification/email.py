# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: miha@reciprocitylabs.com


"""
 GGRC email notification module hook to prepares email, email digest, notify
 email to recipients
"""


from google.appengine.api import mail
from ggrc import settings
from flask import current_app


def getAppEngineEmail():
  email = getattr(settings, 'APPENGINE_EMAIL')
  return email if mail.is_email_valid(email) else None


def send_email(user_email, subject, body):
  sender = getAppEngineEmail()
  if not mail.is_email_valid(user_email):
    current_app.logger.error("Invalid email: {}".format(user_email))
    return False
  if not sender:
    current_app.logger.error("APPENGINE_EMAIL setting is invalid.")
    return False

  message = mail.EmailMessage(sender=sender, subject=subject)

  message.to = user_email
  message.body = "TODO: add email in text mode."
  message.html = body

  message.send()
  return True

