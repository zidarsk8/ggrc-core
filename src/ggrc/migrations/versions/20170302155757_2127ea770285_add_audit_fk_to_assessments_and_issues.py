# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add audit FK to assessments and issues

Create Date: 2017-03-02 15:57:57.006126
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '2127ea770285'
down_revision = '3f615f3b5192'


def upgrade_table(table_name, model_name):
  op.add_column(
      table_name,
      sa.Column("audit_id", sa.Integer(), nullable=True)
  )
  op.execute("""
      UPDATE {table_name} AS t
      LEFT JOIN relationships AS r ON
        r.source_type = '{model_name}' AND
        r.source_id = t.id AND
        r.destination_type = 'Audit'
      LEFT JOIN audits as a ON
        a.id = r.destination_id
      SET
        t.audit_id = a.id
      WHERE
        t.audit_id is null
  """.format(
      table_name=table_name,
      model_name=model_name,
  ))

  op.execute("""
      UPDATE {table_name} AS t
      LEFT JOIN relationships AS r ON
        r.destination_type = '{model_name}' AND
        r.destination_id = t.id AND
        r.source_type = 'Audit'
      LEFT JOIN audits as a ON
        a.id = r.source_id
      SET
        t.audit_id = a.id
      WHERE
        t.audit_id is null
  """.format(
      table_name=table_name,
      model_name=model_name,
  ))

  op.create_foreign_key(
      "fk_{}_audits".format(table_name),
      table_name,
      "audits",
      ["audit_id"],
      ["id"],
      ondelete="RESTRICT"
  )


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  import ipdb
  ipdb.set_trace()
  upgrade_table("assessments", "Assessment")
  upgrade_table("issues", "Issue")
  print 5


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
