# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from logging import getLogger
from traceback import format_exc

from ggrc import extensions
from ggrc.notifications import common


# pylint: disable=invalid-name
logger = getLogger(__name__)


def send_error_notification(message):
  try:
    user_email = common.get_app_engine_email()
    common.send_email(user_email, "Error in nightly cron job", message)
  except:  # pylint: disable=bare-except
    logger.exception("Failed on sending notification")


def run_job(job):
  try:
    job()
  except:  # pylint: disable=bare-except
    logger.exception("Job '%s' failed", job.__name__)
    send_error_notification(
        "Job '%s' failed with: \n%s" % (job.__name__, format_exc())
    )


def nightly_cron_endpoint():
  cron_jobs = extensions.get_module_contributions("CONTRIBUTED_CRON_JOBS")
  for job in cron_jobs:
    run_job(job)
  return 'Ok'


def init_cron_views(app):
  app.add_url_rule(
      "/nightly_cron_endpoint", "nightly_cron_endpoint",
      view_func=nightly_cron_endpoint)
