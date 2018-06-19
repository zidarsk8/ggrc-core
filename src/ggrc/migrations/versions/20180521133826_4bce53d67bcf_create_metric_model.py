# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Create Metric model

Create Date: 2018-05-21 13:38:26.866299
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

from ggrc.migrations.utils import acr_propagation_document_epic \
    as prev_rules
from ggrc.migrations.utils import acr_propagation_constants_metric \
    as metric_rules
from ggrc.migrations.utils import acr_propagation
from ggrc.migrations.utils import update_acr

# revision identifiers, used by Alembic.
revision = '4bce53d67bcf'
down_revision = '2efe5292b7ac'


NON_EDITABLE_ROLES = {
    "Primary Contacts",
    "Secondary Contacts",
}


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.create_table(
      'metrics',
      # Base, Identifiable, Id
      sa.Column('id', sa.Integer(), nullable=False),
      # BisinessObject, Titled, title
      sa.Column('title', sa.String(length=250), nullable=False),
      # BusinessObject, Described, description
      sa.Column('description', sa.Text(), nullable=False),
      # BusinessObject, Noted, Notes
      sa.Column('notes', sa.Text(), nullable=False),
      # BusinessObject, Slugged, Code
      sa.Column('slug', sa.String(length=250), nullable=False),
      # BusinessObject, Stateful, State
      sa.Column('status', sa.String(length=250),
                nullable=False, server_default="Draft"),
      # HasObjectState, Review State
      sa.Column('os_state', sa.String(length=16),
                nullable=False, server_default="Unreviewed"),
      # TestPlanned, Assessment Procedure
      sa.Column('test_plan', sa.Text(), nullable=False),
      # ObjectPerson, Timeboxed, WithStartDate, Effective Date
      sa.Column('start_date', sa.Date(), nullable=True),
      # LastDeprecatedTimeboxed, Last Deprecated Date
      sa.Column('end_date', sa.Date(), nullable=True),
      # Commentable, Recipients
      sa.Column('recipients', sa.String(length=250), nullable=True),
      # Commentable, Send by default
      sa.Column('send_by_default', mysql.TINYINT(display_width=1),
                nullable=True),
      # Base, ContextRBAC, Context Id
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=False),
      sa.Column('updated_at', sa.DateTime(), nullable=False),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),

      sa.PrimaryKeyConstraint('id'),
      mysql_default_charset=u'utf8',
      mysql_engine=u'InnoDB',
  )
  op.create_foreign_key(
      None,
      'metrics',
      'contexts',
      ['context_id'], ['id']
  )
  op.create_index(
      'fk_metrics_contexts',
      'metrics',
      ['context_id'],
      unique=False
  )
  op.create_index(
      'ix_metrics_updated_at',
      'metrics',
      ['updated_at'],
      unique=False
  )
  op.create_unique_constraint(
      'uq_metrics',
      'metrics',
      ['slug']
  )
  op.create_unique_constraint(
      'uq_t_metrics',
      'metrics',
      ['title']
  )
  update_acr.update_models_with_contacts(['Metric'], NON_EDITABLE_ROLES)
  update_acr.update_ownable_models(['Metric'])

  acr_propagation.update_acr_propagation_tree(
      prev_rules.GGRC_PROPAGATION,
      metric_rules.GGRC_PROPAGATION
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_table('metrics')

  acr_propagation.update_acr_propagation_tree(
      metric_rules.GGRC_PROPAGATION,
      prev_rules.GGRC_PROPAGATION
  )

  # Remove items from access_control_list
  op.execute("DELETE FROM access_control_list "
             "WHERE object_type = 'Metric'")
  # Remove items from access_control_roles
  op.execute("DELETE FROM access_control_roles "
             "WHERE object_type = 'Metric'")
