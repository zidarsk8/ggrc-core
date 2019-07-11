# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""This module provides endpoints to validate Issue Tracker issue ID."""

import json

import flask

from ggrc import login
from ggrc import utils as ggrc_utils
from ggrc.integrations import constants as integration_constants
from ggrc.integrations import utils as integration_utils
from ggrc.models import issuetracker_issue


@login.login_required
def validate_issue(issue_id):
  """Validate Issue Tracker issue ID."""
  with ggrc_utils.benchmark("Validate Issue Tracker issue ID"):
    msg, valid, linked_resource = u"", True, None

    if not integration_utils.has_access_to_issue(issue_id):
      msg = integration_constants.TICKET_NO_ACCESS_TMPL
      valid = False
    else:
      issue_model = issuetracker_issue.IssuetrackerIssue
      linked_resource = issue_model.query.filter(
          issue_model.issue_id == issue_id,
      ).first()

      if linked_resource is not None:
        msg = integration_constants.TICKET_ALREADY_LINKED_TMPL
        valid = False

  response_body = {
      "type": getattr(linked_resource, "object_type", None),
      "id": getattr(linked_resource, "object_id", None),
      "valid": valid,
      "msg": msg,
  }

  return flask.make_response((
      json.dumps(response_body), 200, [("Content-Type", "application/json")]
  ))


def init_issue_tracker_views(app):
  """Initializer for issue tracker views."""

  app.add_url_rule(
      "/api/validate_issue/<int:issue_id>",
      "validate_issue_tracker_issue_id",
      view_func=validate_issue,
  )
