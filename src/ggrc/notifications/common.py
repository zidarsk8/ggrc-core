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
  """Get notification sender email.

  Return the email of the user that will be set as sender. This email should be
  authorized to send emails from the server. For more details, see Application
  Settins for email api authorized senders.

  Returns:
    Valid email address if it's set in the app settings.
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
  """
  sender = getAppEngineEmail()
  if not mail.is_email_valid(user_email):
    current_app.logger.error("Invalid email recipient: {}".format(user_email))
    return
  if not sender:
    current_app.logger.error("APPENGINE_EMAIL setting is invalid.")
    return

  message = mail.EmailMessage(sender=sender, subject=subject)

  message.to = user_email
  message.body = "TODO: add email in text mode."
  message.html = body

  message.send()
