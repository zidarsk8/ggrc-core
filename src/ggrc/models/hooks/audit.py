# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
  Audit permission hooks

  The following permission hooks make sure archived audits are not editable
"""
from werkzeug.exceptions import Forbidden

from ggrc import db
from ggrc.models import all_models
from ggrc.services import signals


def init_hook():
  """Init audit permission hooks"""
  # pylint: disable=unused-variable
  @signals.Restful.model_put.connect_via(all_models.Audit)
  @signals.Restful.model_deleted.connect_via(all_models.Audit)
  def handle_audit_permission_put(sender, obj, src, service=None):
    """Make sure admins cannot delete/update archived audits"""
    # pylint: disable=unused-argument
    if obj.archived and not db.inspect(
       obj).get_history('archived', False).has_changes():
      raise Forbidden()

  # pylint: disable=unused-variable
  @signals.Restful.model_put.connect_via(all_models.Snapshot)
  @signals.Restful.model_put.connect_via(all_models.Issue)
  @signals.Restful.model_deleted.connect_via(all_models.Issue)
  @signals.Restful.model_put.connect_via(all_models.Assessment)
  @signals.Restful.model_deleted.connect_via(all_models.Assessment)
  def handle_archived_issue(sender, obj=None, src=None, service=None):
    """Make sure admins cannot delete/update archived audits"""
    # pylint: disable=unused-argument
    if obj.archived:
      raise Forbidden()
