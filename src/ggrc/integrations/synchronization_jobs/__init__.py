# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Contains integration functionality with issue tracker via cron jobs."""

from ggrc.integrations.synchronization_jobs.assessment_sync_job import \
    sync_assessment_statuses  # Noqa
from ggrc.integrations.synchronization_jobs.issue_sync_job import \
    sync_issue_attributes  # Noqa
