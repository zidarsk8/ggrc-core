# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Package contains RBAC related helper functions."""

from ggrc.models import all_models


class RBACHelper(object):  # pylint: disable=too-few-public-methods
  """RBAC related helper.

  Attributes:
      g_roles: Mapping like {'Global Role Name': Role instance}.
  """
  GR_RNAME = "Reader"
  GE_RNAME = "Editor"
  GA_RNAME = "Administrator"
  GC_RNAME = "Creator"

  def __init__(self):
    global_rnames = (
        self.GR_RNAME,
        self.GE_RNAME,
        self.GA_RNAME,
        self.GC_RNAME,
    )
    self.g_roles = {
        r.name: r
        for r in all_models.Role.query.filter(
            all_models.Role.name.in_(global_rnames))
    }
