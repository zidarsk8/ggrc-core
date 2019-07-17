# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
remove proposal data related to control model

Create Date: 2019-07-16 11:15:53.675414
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = 'a6b61113e372'
down_revision = '17fbb17f7cec'


def remove_relationships(conn):
  """Remove old control relationships"""
  conn.execute(
      sa.text("DELETE FROM relationships WHERE "
              "source_type = 'Control' AND destination_type = 'Proposal'"
              ),
  )


def remove_proposal_and_comments(conn):
  """Remove old proposals for controls"""
  conn.execute(
      sa.text("DELETE FROM proposals WHERE instance_type = 'Control'"),
  )


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  conn = op.get_bind()
  remove_relationships(conn)
  remove_proposal_and_comments(conn)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
