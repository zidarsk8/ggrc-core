# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Change relationship between assessment templates and audits not null

Create Date: 2018-05-08 14:52:25.534107
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9bc9e8064e04'
down_revision = 'ad7e10f2a917'


def remove_assessment_templates():
  """Remove assessment_templates with empty audit_id"""
  op.execute("""
      DELETE ast from assessment_templates ast WHERE ast.audit_id IS NULL
  """)


def alter_constraints():
  """Update fk_assessment_template_audits constraint"""
  op.drop_constraint("fk_assessment_template_audits", "assessment_templates",
                     "foreignkey")

  op.alter_column("assessment_templates", "audit_id",
                  existing_type=sa.Integer(),
                  nullable=False)

  op.create_foreign_key(constraint_name="fk_assessment_template_audits",
                        source_table="assessment_templates",
                        referent_table="audits",
                        local_cols=["audit_id"],
                        remote_cols=["id"])


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  remove_assessment_templates()
  alter_constraints()


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""

  op.drop_constraint("fk_assessment_template_audits", "assessment_templates",
                     "foreignkey")

  op.alter_column("assessment_templates", "audit_id",
                  existing_type=sa.Integer(),
                  nullable=True)

  op.create_foreign_key(constraint_name="fk_assessment_template_audits",
                        source_table="assessment_templates",
                        referent_table="audits",
                        local_cols=["audit_id"],
                        remote_cols=["id"],
                        ondelete='SET NULL')
