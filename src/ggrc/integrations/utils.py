# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module provides various utils for Issue tracker integration service."""

import logging
import time

from sqlalchemy.sql import expression

from ggrc import models
from ggrc.integrations import integrations_errors
from ggrc.integrations import issues


logger = logging.getLogger(__name__)


_BATCH_SIZE = 100

# A list of field to watch for changes in.
_FIELDS_TO_CHECK = ('status', 'type', 'priority', 'severity')


def _collect_assessment_issues():
  """Returns issue infos associated with Assessments."""
  issue_params = {}

  issuetracker_cls = models.IssuetrackerIssue
  issue_objects = issuetracker_cls.query.filter(
      issuetracker_cls.object_type == 'Assessment',
      issuetracker_cls.enabled == expression.true(),
      issuetracker_cls.issue_id.isnot(None),
  ).order_by(issuetracker_cls.object_id).all()
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


def _iter_issue_batches(ids):
  """Generates a sequence of batches of issues from Issue Tracker by IDs."""
  cli = issues.Client()

  for i in xrange(0, len(ids), _BATCH_SIZE):
    chunk = ids[i:i + _BATCH_SIZE]
    logger.debug('Issue ids to process: %s', chunk)
    try:
      response = cli.search({
          'issue_ids': chunk,
          'page_size': _BATCH_SIZE,
      })
    except integrations_errors.HttpError as error:
      logger.error(
          'Unable to fetch Issue Tracker issues by IDs: %r', error)
      return

    issue_infos = {}
    response_issues = response.get('issues') or []
    for info in response_issues:
      state = info['issueState'] or {}
      issue_infos[info['issueId']] = {
          'status': state.get('status'),
          'type': state.get('type'),
          'priority': state.get('priority'),
          'severity': state.get('severity'),
      }
    if issue_infos:
      yield issue_infos


def _update_issue(cli, issue_id, params, max_attempts=5, interval=1):
  """Performs issue update request."""
  attempts = max_attempts
  while True:
    attempts -= 1
    try:
      cli.update_issue(issue_id, params)
    except integrations_errors.HttpError as error:
      if error.status == 429:
        if attempts == 0:
          raise
        logger.warning(
            'The request updating ticket ID=%s was '
            'rate limited and will be re-tried: %s', issue_id, error)
        time.sleep(interval)
        continue
    break


def sync_issue_tracker_statuses():
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
  for batch in _iter_issue_batches(list(assessment_issues)):
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
          for field in _FIELDS_TO_CHECK
      ):
        continue

      try:
        _update_issue(cli, issue_id, assessment_state)
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
