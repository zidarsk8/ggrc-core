# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module contains functionality for issue with issue tracker integration."""

# pylint: disable=unused-argument
# pylint: disable=no-else-return

import logging


from ggrc import db
from ggrc.integrations import issues
from ggrc.integrations import integrations_errors
from ggrc.models import all_models
from ggrc.models.hooks.issue_tracker import issue_tracker_params_builder
from ggrc.models.hooks.issue_tracker import integration_utils
from ggrc.utils.custom_dict import MissingKeyDict

logger = logging.getLogger(__name__)


ISSUE_TRACKER_FIELDS_TO_UPDATE = ("component_id", "hotlist_id",
                                  "severity", "priority")


ISSUE_TRACKER_TO_DB_NAME_MAPPING = MissingKeyDict({
    "severity": "issue_severity",
    "priority": "issue_priority"
})


def build_issue_tracker_attrs(query):
  """Create dictionary to update IssuetrackerIssue from query

  Rename keys because of different naming in db and in issue tracker
  """
  name_mapping = ISSUE_TRACKER_TO_DB_NAME_MAPPING
  fields_to_update = ISSUE_TRACKER_FIELDS_TO_UPDATE
  return {name_mapping[field]: query[field] for field in fields_to_update
          if field in query}


def create_issue_handler(obj, issue_tracker_info):
  """Event handler for issue object creation."""
  if not issue_tracker_info or not issue_tracker_info.get("enabled"):
    return

  # We need in flush here because we need object id for URL generation.
  db.session.flush()

  builder = issue_tracker_params_builder.IssueParamsBuilder()
  issue_tracker_query = builder.build_create_issue_tracker_params(
      obj,
      issue_tracker_info
  )

  if not issue_tracker_query:
    return

  # Try to create issue in issue tracker.
  try:
    res = issues.Client().create_issue(issue_tracker_query)

    issue_url = integration_utils.build_issue_tracker_url(res["issueId"])
    issue_tracker_info["issue_url"] = issue_url
    issue_tracker_info["issue_id"] = res["issueId"]
  except integrations_errors.Error as error:
    logger.error(
        "Unable to create a ticket while creating object ID=%d: %s",
        obj.id, error
    )
    obj.add_warning("Unable to create a ticket in issue tracker.")
    issue_tracker_info["enabled"] = False

  # Fill necessary fields for issuetracker_issue object.
  issue_tracker_info["cc_list"] = issue_tracker_query["ccs"]
  issue_tracker_info["assignee"] = issue_tracker_query["assignee"]
  issue_tracker_info["title"] = issue_tracker_query["title"]

  # Create object in GGRC with info about issue tracker integration.
  all_models.IssuetrackerIssue.create_or_update_from_dict(
      obj, issue_tracker_info
  )


def delete_issue_handler(obj, **kwargs):
  """Event handler for issue object deletion."""
  issue_tracker_object = all_models.IssuetrackerIssue.get_issue("Issue",
                                                                obj.id)

  if issue_tracker_object:
    if issue_tracker_object.enabled and issue_tracker_object.issue_id:
      builder = issue_tracker_params_builder.IssueParamsBuilder()
      issue_tracker_query = builder.build_delete_issue_tracker_params()
      try:
        issues.Client().update_issue(issue_tracker_object.issue_id,
                                     issue_tracker_query)
      except integrations_errors.Error as error:
        logger.error("Unable to update a ticket ID=%s while deleting"
                     " issue ID=%d: %s",
                     issue_tracker_object.issue_id, obj.id, error)
        obj.add_warning("Unable to update a ticket in issue tracker.")
    db.session.delete(issue_tracker_object)


def update_issue_handler(obj, initial_state, new_issue_tracker_info=None):
  """Event handler for issue object renewal."""
  issue_tracker_object = all_models.IssuetrackerIssue.get_issue("Issue",
                                                                obj.id)

  if not issue_tracker_object:
    if new_issue_tracker_info and new_issue_tracker_info["enabled"]:
      create_issue_handler(obj, new_issue_tracker_info)
    return

  current_issue_tracker_info = issue_tracker_object.to_dict(
      include_issue=True,
      include_private=True
  )

  if not new_issue_tracker_info:
    # Use existing issue tracker info if object is updating via import
    new_issue_tracker_info = current_issue_tracker_info

  # Build query
  builder = issue_tracker_params_builder.IssueParamsBuilder()
  query = builder.build_update_issue_tracker_params(
      obj,
      initial_state,
      new_issue_tracker_info,
      current_issue_tracker_info
  )

  if query:
    try:
      issues.Client().update_issue(issue_tracker_object.issue_id, query)
    except integrations_errors.Error as error:
      logger.error("Unable to update a ticket ID=%s while deleting"
                   " issue ID=%d: %s",
                   issue_tracker_object.issue_id, obj.id, error)
      obj.add_warning("Unable to update a ticket in issue tracker.")

  issue_tracker_attrs = build_issue_tracker_attrs(query)
  if issue_tracker_attrs:
    current_issue_tracker_info.update(issue_tracker_attrs)
    current_issue_tracker_info["enabled"] = new_issue_tracker_info["enabled"]
    all_models.IssuetrackerIssue.create_or_update_from_dict(
        obj, current_issue_tracker_info
    )
