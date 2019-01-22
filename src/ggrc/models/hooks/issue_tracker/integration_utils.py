# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""This module contains common utils for integration functionality."""

import sqlalchemy as sa

from ggrc import db
from ggrc import settings
from ggrc.models import exceptions
from ggrc.models import all_models
from ggrc.integrations import constants


def is_already_linked(ticket_id):
  """Checks if ticket with ticket_id is already linked to GGRC object"""
  exists_query = db.session.query(
      all_models.IssuetrackerIssue.issue_id
  ).filter_by(issue_id=ticket_id).exists()
  return db.session.query(exists_query).scalar()


def normalize_issue_tracker_info(info):
  """Insures that component ID and hotlist ID are integers."""
  # TODO(anushovan): remove data type casting once integration service
  #   supports strings for following properties.
  component_id = info.get('component_id')
  if component_id:
    try:
      info['component_id'] = int(component_id)
    except (TypeError, ValueError):
      raise exceptions.ValidationError('Component ID must be a number.')

  hotlist_id = info.get('hotlist_id')
  if hotlist_id:
    try:
      info['hotlist_id'] = int(hotlist_id)
    except (TypeError, ValueError):
      raise exceptions.ValidationError('Hotlist ID must be a number.')


def set_values_for_missed_fields(assmt, issue_tracker_info):
  """Set values for empty issue tracked fields.

  Current list of fields with default values: component_id, hotlist_id,
    issue_type, priority, severity. They would be taken from default values if
    they are empty in appropriate audit.
  Current list of values that would be taken from assessment: title, status,
    due date.
  """
  audit_info = assmt.audit.issue_tracker or {}
  default_values = constants.DEFAULT_ISSUETRACKER_VALUES
  if not issue_tracker_info.get("component_id"):
    issue_tracker_info["component_id"] = audit_info.get("component_id") or\
        default_values["component_id"]

  if not issue_tracker_info.get("hotlist_id"):
    issue_tracker_info["hotlist_id"] = audit_info.get("hotlist_id") or\
        default_values["hotlist_id"]

  if not issue_tracker_info.get("issue_type"):
    issue_tracker_info["issue_type"] = audit_info.get("issue_type") or\
        default_values["issue_type"]

  if not issue_tracker_info.get("issue_priority"):
    issue_tracker_info["issue_priority"] = audit_info.get("issue_priority") or\
        default_values["issue_priority"]

  if not issue_tracker_info.get("issue_severity"):
    issue_tracker_info["issue_severity"] = audit_info.get("issue_severity") or\
        default_values["issue_severity"]

  if not issue_tracker_info.get("title"):
    issue_tracker_info["title"] = assmt.title

  if not issue_tracker_info.get("status"):
    issue_tracker_info["status"] = constants.STATUSES_MAPPING.get(
        assmt.status
    )

  if not issue_tracker_info.get('due_date'):
    issue_tracker_info['due_date'] = assmt.start_date


def build_issue_tracker_url(issue_id):
  """Build issue tracker URL by issue id."""
  issue_tracker_tmpl = settings.ISSUE_TRACKER_BUG_URL_TMPL
  url_tmpl = issue_tracker_tmpl if issue_tracker_tmpl else 'http://issue/%s'
  return url_tmpl % issue_id


def exclude_auditor_emails(emails):
  """Returns new email set with excluded auditor emails."""
  acl = all_models.AccessControlList
  acr = all_models.AccessControlRole
  acp = all_models.AccessControlPerson

  if not isinstance(emails, set):
    emails = set(emails)

  auditor_emails = db.session.query(
      all_models.Person.email
  ).join(
      acp
  ).join(
      acl
  ).join(
      acr
  ).filter(
      acr.name == "Auditors",
      all_models.Person.email.in_(emails)
  ).distinct().all()

  emails_to_exlude = {line.email for line in auditor_emails}
  return emails - emails_to_exlude


def build_created_objects_args(revision_ids, mail_data):
  """Build params for bulk ticket create."""
  objects = _collect_created_objects(revision_ids)

  return _create_args(objects, mail_data)


def build_updated_objects_args(revision_ids, mail_data):
  """Build params for bulk ticket update."""
  objects = _collect_update_objects(revision_ids)

  return _create_args(objects, mail_data)


def build_comments_args(revision_ids, mail_data):
  """Build params for bulk Issue Tracker comments update."""
  comments = _collect_comments(revision_ids)
  arg_list = {}
  arg_list["comments"] = [{
      "type": obj[0],
      "id": int(obj[1]),
      "comment_description": obj[2]
  } for obj in comments]

  arg_list["mail_data"] = mail_data
  return arg_list


def _create_args(objects, mail_data):
  """Create args to call bulk update/create"""

  if not objects:
    return {}

  arg_list = {}
  arg_list["objects"] = [
      {"type": obj[0], "id": int(obj[1])} for obj in objects
  ]
  arg_list["mail_data"] = mail_data
  return arg_list


def _collect_created_objects(revision_ids):
  """Collect all issuetracked models and issuetracker issues for create.

  Args:
      revision_ids: list of revision ids we should look through.
  Returns:
      list of issuetracked objects that were imported.
  """

  revisions = all_models.Revision
  iti = all_models.IssuetrackerIssue

  issue_tracked_objects = db.session.query(
      revisions.resource_type,
      revisions.resource_id,
  ).join(
      iti,
      sa.and_(
          revisions.resource_type == iti.object_type,
          revisions.resource_id == iti.object_id
      )
  ).filter(
      revisions.resource_type.in_(constants.ISSUE_TRACKED_MODELS),
      revisions.id.in_(revision_ids),
      iti.issue_id.is_(None),
      iti.enabled != 0,
  )

  iti_related_objects = db.session.query(
      iti.object_type,
      iti.object_id,
  ).join(
      revisions,
      revisions.resource_id == iti.id,
  ).filter(
      revisions.resource_type == "IssuetrackerIssue",
      revisions.id.in_(revision_ids),
      iti.object_type.in_(constants.ISSUE_TRACKED_MODELS),
      iti.issue_id.is_(None),
      iti.enabled != 0,
  )

  return issue_tracked_objects.union(iti_related_objects).all()


def _collect_update_objects(revision_ids):
  """Collect all issuetracked models and issuetracker issues for update.

  Args:
      revision_ids: list of revision ids we should look through.
  Returns:
      list of issuetracked objects that were imported.
  """

  revisions = all_models.Revision
  iti = all_models.IssuetrackerIssue

  issue_tracked_objects = db.session.query(
      revisions.resource_type,
      revisions.resource_id,
  ).join(
      iti,
      sa.and_(
          revisions.resource_type == iti.object_type,
          revisions.resource_id == iti.object_id
      )
  ).filter(
      revisions.resource_type.in_(constants.ISSUE_TRACKED_MODELS),
      revisions.id.in_(revision_ids),
      iti.issue_id.isnot(None),
      iti.enabled != 0,
  )

  iti_related_objects = db.session.query(
      iti.object_type,
      iti.object_id,
  ).join(
      revisions,
      revisions.resource_id == iti.id,
  ).filter(
      revisions.resource_type == "IssuetrackerIssue",
      revisions.id.in_(revision_ids),
      iti.object_type.in_(constants.ISSUE_TRACKED_MODELS),
      iti.issue_id.isnot(None),
      iti.enabled != 0,
  )

  return issue_tracked_objects.union(iti_related_objects).all()


def _collect_comments(revision_ids):
  """Collect all comments to issuetracked models.

     Args:
         revision_ids: list of revision ids we should look through
     Returns:
         list of comments that were imported.
   """
  revisions = all_models.Revision
  comments = all_models.Comment

  imported_comments_src = db.session.query(
      revisions.destination_type,
      revisions.destination_id,
      comments.description,
  ).join(
      comments,
      revisions.source_id == comments.id,
  ).filter(
      revisions.resource_type == "Relationship",
      revisions.source_type == "Comment",
      revisions.id.in_(revision_ids),
      revisions.destination_type.in_(constants.ISSUE_TRACKED_MODELS)
  )

  imported_comments_dst = db.session.query(
      revisions.source_type,
      revisions.source_id,
      comments.description,
  ).join(
      comments,
      revisions.destination_id == comments.id,
  ).filter(
      revisions.resource_type == "Relationship",
      revisions.destination_type == "Comment",
      revisions.id.in_(revision_ids),
      revisions.source_type.in_(constants.ISSUE_TRACKED_MODELS)
  )
  return imported_comments_dst.union(imported_comments_src).all()
