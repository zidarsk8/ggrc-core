# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import traceback
from flask import current_app

from ggrc.notification import email


def send_error_notification(message):
  try:
    user_email = email.getAppEngineEmail()
    email.send_email(user_email, "Error in nightly cron job", message)
  except Exception as e:
    current_app.logger.error(e)


def run_job(job):
  try:
    job()
  except:
    message = "job '{}' failed with: \n{}".format(job.__name__,
                                                  traceback.format_exc())
    current_app.logger.error(message)
    send_error_notification(message)


def nightly_cron_endpoint():
  from ggrc_workflows.views import send_todays_digest_notifications
  from ggrc_workflows import start_recurring_cycles
  cron_jobs = [
      start_recurring_cycles,
      send_todays_digest_notifications
  ]

  for job in cron_jobs:
    run_job(job)

  return 'Ok'


def init_cron_views(app):
  app.add_url_rule(
      "/nightly_cron_endpoint", "nightly_cron_endpoint",
      view_func=nightly_cron_endpoint)
