# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
  Audit permission hooks

  The following permission hooks make sure archived audits are not editable
"""
import itertools

from werkzeug.exceptions import Forbidden

from ggrc import db
from ggrc.models import all_models
from ggrc.services import signals


_AUDIT_MODEL_NAME = 'Audit'


@signals.Restful.collection_posted.connect_via(all_models.Audit)
def handle_audit_post(sender, objects=None, sources=None):
  """Handles creating issue tracker related info."""
  del sender  # Unused
  for obj, src in itertools.izip(objects, sources):
    issue_tracker_info = src.get('issue_tracker')
    if not issue_tracker_info:
      continue
    all_models.IssuetrackerIssue.create_or_update_from_dict(
        _AUDIT_MODEL_NAME, obj.id, issue_tracker_info)


@signals.Restful.model_put.connect_via(all_models.Audit)
def handle_audit_put(sender, obj=None, src=None, service=None):
  """Handles updating issue tracker related info."""
  del sender, service  # Unused
  issue_tracker_info = src.get('issue_tracker')
  if issue_tracker_info:
    all_models.IssuetrackerIssue.create_or_update_from_dict(
        _AUDIT_MODEL_NAME, obj.id, issue_tracker_info)


@signals.Restful.model_deleted_after_commit.connect_via(all_models.Audit)
def handle_audit_deleted_after_commit(sender, obj=None, service=None,
                                      event=None):
  """Handles deleting issue tracker related info."""
  del sender, service, event  # Unused
  issue_obj = all_models.IssuetrackerIssue.get_issue(
      _AUDIT_MODEL_NAME, obj.id)
  if issue_obj:
    db.session.delete(issue_obj)


def init_hook():
  """Initializes audit permission hooks."""
  # pylint: disable=unused-variable
  @signals.Restful.model_put.connect_via(all_models.Audit)
  @signals.Restful.model_deleted.connect_via(all_models.Audit)
  def handle_audit_permission_put(sender, obj, src=None, service=None):
    """Make sure admins cannot delete/update archived audits"""
    # pylint: disable=unused-argument
    if obj.archived and not db.inspect(
       obj).get_history('archived', False).has_changes():
      raise Forbidden()

  # pylint: disable=unused-variable
  @signals.Restful.model_deleted.connect_via(all_models.Assessment)
  @signals.Restful.model_deleted.connect_via(all_models.AssessmentTemplate)
  @signals.Restful.model_posted.connect_via(all_models.Assessment)
  @signals.Restful.model_posted.connect_via(all_models.AssessmentTemplate)
  @signals.Restful.model_put.connect_via(all_models.Assessment)
  @signals.Restful.model_put.connect_via(all_models.AssessmentTemplate)
  @signals.Restful.model_put.connect_via(all_models.Snapshot)
  def handle_archived_object(sender, obj=None, src=None, service=None):
    """Make sure admins cannot delete/update archived audits"""
    # pylint: disable=unused-argument
    if obj.archived:
      raise Forbidden()

  @signals.Restful.model_deleted.connect_via(all_models.Comment)
  @signals.Restful.model_deleted.connect_via(all_models.Document)
  @signals.Restful.model_deleted.connect_via(all_models.UserRole)
  @signals.Restful.model_posted.connect_via(all_models.Comment)
  @signals.Restful.model_posted.connect_via(all_models.Document)
  @signals.Restful.model_posted.connect_via(all_models.Snapshot)
  @signals.Restful.model_posted.connect_via(all_models.UserRole)
  def handle_archived_context(sender, obj=None, src=None, service=None):
    """Make sure admins cannot delete/update archived audits"""
    # pylint: disable=unused-argument
    if (hasattr(obj, 'context') and
        hasattr(obj.context, 'related_object') and getattr(
            obj.context.related_object, 'archived', False)):
      raise Forbidden()

  @signals.Restful.model_posted.connect_via(all_models.Relationship)
  @signals.Restful.model_deleted.connect_via(all_models.Relationship)
  def handle_archived_relationships(sender, obj=None, src=None, service=None):
    """Make sure users can not map objects to archived audits"""
    # pylint: disable=unused-argument
    if (getattr(obj, 'source_type', None) == 'Issue' or
       getattr(obj, 'destination_type', None) == 'Issue'):
      # Issues can be mapped even if audit is archived so skip the permission
      # check here
      return
    if (hasattr(obj, 'context') and
        hasattr(obj.context, 'related_object') and getattr(
            obj.context.related_object, 'archived', False)):
      raise Forbidden()
