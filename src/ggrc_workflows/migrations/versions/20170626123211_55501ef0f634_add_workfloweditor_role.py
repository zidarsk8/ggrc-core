# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add WorkflowEditor permission role

Create Date: 2017-06-26 12:32:11.421317
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name
import sqlalchemy

from ggrc import db
from ggrc_basic_permissions import Role

# revision identifiers, used by Alembic.
revision = '55501ef0f634'
down_revision = '50788b66dcd4'

_NOW = sqlalchemy.func.now()


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  db.session.add(Role(
      name="WorkflowEditor",
      permissions_json="CODE DECLARED ROLE",
      description="This role grants a user permission to edit workflow "
                  "mappings and details",
      created_at=_NOW,
      updated_at=_NOW,
      scope="Workflow Implied"
  ))
  db.session.commit()


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  wf_editor_role = Role.query.filter_by(name="WorkflowEditor").first()
  db.session.delete(wf_editor_role)
  db.session.commit()
