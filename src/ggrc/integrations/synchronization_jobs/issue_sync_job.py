# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Issue object integration functionality via cron job."""

import logging

from ggrc import db
from ggrc.models import all_models
from ggrc.integrations.synchronization_jobs import sync_utils


logger = logging.getLogger(__name__)


FIELDS_TO_CHECK = ()


ISSUE_STATUS_MAPPING = {
    "new": "Draft",
    "assigned": "Draft",
    "accepted": "Active",
    "fixed": "Fixed",
    "verified": "Fixed and Verified",
    "not reproducible": "Deprecated",
    "intended behaviour": "Deprecated",
    "obsolete": "Deprecated",
    "infeasible": "Deprecated",
    "duplicate": "Deprecated",
}


def sync_assignee_email(issuetracker_state, sync_object, assignees_role):
  """Sync issue assignee email."""
  issue_tracker_assignee = issuetracker_state.get("assignee")
  new_assignee = all_models.Person.query.filter_by(
      email=issue_tracker_assignee
  ).first()
  if new_assignee:
    issue_primary_contacts = sync_object.get_persons_for_rolename(
      "Primary Contacts"
    )
    if issue_tracker_assignee not in issue_primary_contacts:
      sync_object.extend_access_control_list([{
        "ac_role": assignees_role,
        "person": new_assignee
      }])


def sync_verifier_email(issuetracker_state, sync_object, admin_role):
  """Sync Issue verifier email."""
  issue_tracker_verifier = issuetracker_state.get("verifier")
  new_verifier = all_models.Person.query.filter_by(
        email=issue_tracker_verifier
  ).first()
  if new_verifier:
    issue_admins = sync_object.get_persons_for_rolename("Admin")
    if issue_tracker_verifier not in issue_admins:
      sync_object.extend_access_control_list([{
        "ac_role": admin_role,
        "person": new_verifier
      }])


def sync_statuses(issuetracker_state, sync_object):
  """Sync issue object statuses."""
  issue_tracker_status = issuetracker_state.get("status")
  if issue_tracker_status:
    issue_tracker_status = issue_tracker_status.lower()
  if ISSUE_STATUS_MAPPING[issue_tracker_status] != sync_object.status:
    sync_object.status = ISSUE_STATUS_MAPPING[issue_tracker_status]


def sync_issue_attributes():
  """Synchronizes issue tracker ticket attrs with the Issue object attrs.

  Synchronize issue status and email list (Primary contacts and Admins).
  """
  issuetracker_issues = sync_utils.collect_issue_tracker_info(
      "Issue",
      include_object=True
  )

  if not issuetracker_issues:
    return

  assignees_role = all_models.AccessControlRole.query.filter_by(
      object_type=all_models.Issue.__name__, name="Primary Contacts"
  ).first()

  admin_role = all_models.AccessControlRole.query.filter_by(
      object_type=all_models.Issue.__name__, name="Admin"
  ).first()

  processed_ids = set()
  for batch in sync_utils.iter_issue_batches(issuetracker_issues.keys(),
                                             include_emails=True):
    for issue_id, issuetracker_state in batch.iteritems():
      issue_id = str(issue_id)
      issue_info = issuetracker_issues.get(issue_id)
      if not issue_info:
        logger.warning(
            "Got an unexpected issue from Issue Tracker: %s", issue_id)
        continue

      processed_ids.add(issue_id)
      sync_object = issue_info["object"]

      # Sync attributes.
      sync_statuses(issuetracker_state, sync_object)
      sync_assignee_email(issuetracker_state, sync_object, assignees_role)
      sync_verifier_email(issuetracker_state, sync_object, admin_role)


  db.session.commit()
  logger.debug("Sync is done, %d issue(s) were processed.", len(processed_ids))

  missing_ids = set(issuetracker_issues) - processed_ids
  if missing_ids:
    logger.warning(
        "Some issues are linked to Issue "
        "but were not found in Issue Tracker: %s",
        ", ".join(str(i) for i in missing_ids)
    )
