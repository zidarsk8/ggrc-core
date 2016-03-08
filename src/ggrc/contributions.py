# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Lists of ggrc contributions."""

from ggrc.notifications import send_todays_digest_notifications

CONTRIBUTED_CRON_JOBS = [
    send_todays_digest_notifications
]
