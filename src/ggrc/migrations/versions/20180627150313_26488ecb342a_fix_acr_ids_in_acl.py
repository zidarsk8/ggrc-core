# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Fix ACR ids in ACL.

Create Date: 2018-06-27 15:03:13.237675
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op

# revision identifiers, used by Alembic.
revision = '26488ecb342a'
down_revision = '0e385718442a'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  # We exclude Workflow here as Workflow propagated roles only use
  # two propagated ACRs for all objects so object type is allowed
  # to differ there.
  op.execute("""
      DELETE acl
      FROM access_control_list acl
      JOIN access_control_roles acr ON acl.ac_role_id = acr.id
      WHERE acl.object_type != acr.object_type AND
            acr.object_type != 'Workflow';
  """)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
