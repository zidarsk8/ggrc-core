# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Services for manipulation with daily emails objects via UI."""
from lib import base
from lib.page import daily_emails


class DailyEmailsService(base.WithBrowser):
  """Class for daily emails business layer's services objects."""

  @classmethod
  def open_daily_digest(cls):
    """Open proposal digest."""
    daily_emails.DailyEmails().open_daily_emails_page()

  @classmethod
  def get_email_by_user_name(cls, user_name):
    """Get email by user name."""
    return daily_emails.DailyEmails().get_user_email(user_name)
