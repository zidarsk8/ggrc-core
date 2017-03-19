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
down_revision = '1a5ec1ed04af'


def upgrade_table(table_name):
  """Add audit foreign key to a table."""
  op.add_column(
      table_name,
      sa.Column("audit_id", sa.Integer(), nullable=True)
  )
  op.execute("""
      UPDATE {table_name} AS t
      JOIN contexts AS c ON
          c.id = t.context_id AND
          c.related_object_type = "Audit"
      JOIN audits AS au ON
          c.related_object_id = au.id
      SET
        t.audit_id = au.id
  """.format(
      table_name=table_name,
  ))

  # Simple fix for testing with invalid objects
  op.execute("""
      DELETE FROM {table_name}
      WHERE audit_id IS NULL
  """.format(
      table_name=table_name,
  ))

  op.alter_column(
      table_name,
      "audit_id",
      existing_type=sa.Integer(),
      nullable=False
  )

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
  upgrade_table("assessments")
  upgrade_table("issues")


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_constraint("fk_assessments_audits", "assessments",
                     type_="foreignkey")
  op.drop_constraint("fk_issues_audits", "issues", type_="foreignkey")
  op.drop_column("assessments", "audit_id")
  op.drop_column("issues", "audit_id")
