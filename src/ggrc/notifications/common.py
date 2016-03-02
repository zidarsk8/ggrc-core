# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: miha@reciprocitylabs.com


"""
 GGRC email notification module hook to prepares email, email digest, notify
 email to recipients
"""


from flask import current_app
from google.appengine.api import mail

from ggrc import settings


def getAppEngineEmail():
  """Return a valid email of an appengine user.

  The email that get's returned should be used by appengine as a sender email.
  """
  email = getattr(settings, 'APPENGINE_EMAIL')
  return email if mail.is_email_valid(email) else None


def send_email(user_email, subject, body):
  """Helper function for sending emails.

  Args:
    user_email (string): Email of the recepient.
    subject (string): Email subject.
    body (basestring): Html body of the email. it can contain unicode
      characters and will be sent as a html mime type.

  Returns:
    True if the email was sent or False if something was wrong.
  """
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
