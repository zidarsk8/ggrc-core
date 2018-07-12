# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Create ProductGroup model

Create Date: 2018-07-04 14:48:12.131950
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

from ggrc.migrations.utils import acr_propagation_constants_product_groups \
    as product_group_rules
from ggrc.migrations.utils import acr_propagation
from ggrc.migrations.utils import update_acr

# revision identifiers, used by Alembic.
revision = '84e537a5aede'
down_revision = '5828493ed1ec'


NON_EDITABLE_ROLES = {
    "Primary Contacts",
    "Secondary Contacts",
}


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.create_table(
      'product_groups',
      # Base, Identifiable, Id
      sa.Column('id', sa.Integer(), nullable=False),
      # BusinessObject, Titled, title
      sa.Column('title', sa.String(length=250), nullable=False),
      # BusinessObject, Described, description
      sa.Column('description', sa.Text(), nullable=False),
      # BusinessObject, Noted, Notes
      sa.Column('notes', sa.Text(), nullable=False),
      # BusinessObject, Slugged, Code
      sa.Column('slug', sa.String(length=250), nullable=False),
      # BusinessObject, Stateful, State
      sa.Column('status', sa.String(length=250), nullable=False,
                server_default="Draft"),
      # HasObjectState, Review State
      sa.Column('os_state', sa.String(length=250), nullable=False,
                server_default="Unreviewed"),
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
      'product_groups',
      'contexts',
      ['context_id'], ['id']
  )
  op.create_index(
      'fk_product_groups_contexts',
      'product_groups',
      ['context_id'],
      unique=False
  )
  op.create_index(
      'ix_product_groups_updated_at',
      'product_groups',
      ['updated_at'],
      unique=False
  )
  op.create_unique_constraint(
      'uq_product_groups',
      'product_groups',
      ['slug']
  )
  op.create_unique_constraint(
      'uq_t_product_groups',
      'product_groups',
      ['title']
  )
  update_acr.update_models_with_contacts(['ProductGroup'],
                                         NON_EDITABLE_ROLES)
  update_acr.update_ownable_models(['ProductGroup'])

  acr_propagation.propagate_roles(
      product_group_rules.GGRC_PROPAGATION, with_update=True
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_table('product_groups')

  for object_type, roles_tree in product_group_rules.GGRC_PROPAGATION.items():
    if "ProductGroup" in object_type:
      acr_propagation.remove_propagated_roles(object_type, roles_tree.keys())

  # Remove items from access_control_list
  op.execute("DELETE FROM access_control_list "
             "WHERE object_type = 'ProductGroup'")
  # Remove items from access_control_roles
  op.execute("DELETE FROM access_control_roles "
             "WHERE object_type = 'ProductGroup'")
