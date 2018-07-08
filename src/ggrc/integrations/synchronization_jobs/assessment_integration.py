# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Assessment integration functionality via cron job."""

import logging

from ggrc.integrations import issues, integrations_errors
from ggrc.integrations.synchronization_jobs import utils


logger = logging.getLogger(__name__)


# A list of field to watch for changes in.
FIELDS_TO_CHECK = ('status', 'type', 'priority', 'severity')


def _collect_assessment_issues():
  """Returns issue infos associated with Assessments."""
  issue_params = {}
  issue_objects = utils.get_active_issue_info(model_name="Assessment")
  for iti in issue_objects:
    asmt = iti.issue_tracked_obj
    if not asmt:
      logger.error(
          'The Assessment corresponding to the Issue Tracker Issue ID=%s '
          'does not exist.', iti.issue_id)
      continue

    status_value = issues.STATUSES.get(asmt.status)
    if not status_value:
      logger.error(
          'Inexistent Issue Tracker status for assessment ID=%d '
          'with status: %s.', asmt.id, status_value)
      continue
    issue_params[iti.issue_id] = {
        'assessment_id': asmt.id,
        'state': {
            'status': status_value,
            'type': iti.issue_type,
            'priority': iti.issue_priority,
            'severity': iti.issue_severity,
        },
    }
  return issue_params


def sync_assessment_statuses():
  """Synchronizes issue tracker ticket statuses with the Assessment statuses.

  Checks for Assessments which are in sync with Issue Tracker issues and
  updates their statuses in accordance to the corresponding Assessments
  if differ.
  """
  assessment_issues = _collect_assessment_issues()
  if not assessment_issues:
    return
  logger.debug('Syncing state of %d issues.', len(assessment_issues))

  cli = issues.Client()
  processed_ids = set()
  for batch in utils.iter_issue_batches(list(assessment_issues)):
    for issue_id, issuetracker_state in batch.iteritems():
      issue_id = str(issue_id)
      issue_info = assessment_issues.get(issue_id)
      if not issue_info:
        logger.warning(
            'Got an unexpected issue from Issue Tracker: %s', issue_id)
        continue

      processed_ids.add(issue_id)
      assessment_state = issue_info['state']
      if all(
          assessment_state.get(field) == issuetracker_state.get(field)
          for field in FIELDS_TO_CHECK
      ):
        continue

      try:
        utils.update_issue(cli, issue_id, assessment_state)
      except integrations_errors.Error as error:
        logger.error(
            'Unable to update status of Issue Tracker issue ID=%s for '
            'assessment ID=%d: %r',
            issue_id, issue_info['assessment_id'], error)

  logger.debug('Sync is done, %d issue(s) were processed.', len(processed_ids))

  missing_ids = set(assessment_issues) - processed_ids
  if missing_ids:
    logger.warning(
        'Some issues are linked to Assessments '
        'but were not found in Issue Tracker: %s',
        ', '.join(str(i) for i in missing_ids))
