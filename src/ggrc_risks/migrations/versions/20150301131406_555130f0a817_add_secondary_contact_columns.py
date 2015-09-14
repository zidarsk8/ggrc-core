# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""add secondary contact columns

Revision ID: 555130f0a817
Revises: 44d5969c897b
Create Date: 2015-03-01 13:14:06.935565

"""

# revision identifiers, used by Alembic.
revision = '555130f0a817'
down_revision = '44d5969c897b'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('risks', sa.Column('secondary_contact_id', sa.Integer(), nullable=True))
  op.create_index('fk_risks_secondary_contact', 'risks', ['secondary_contact_id'], unique=False)
  op.add_column('risk_objects', sa.Column('secondary_contact_id', sa.Integer(), nullable=True))
  op.create_index('fk_risk_objects_secondary_contact', 'risk_objects', ['secondary_contact_id'], unique=False)
  op.add_column('threat_actors', sa.Column('secondary_contact_id', sa.Integer(), nullable=True))
  op.create_index('fk_threat_actors_secondary_contact', 'threat_actors', ['secondary_contact_id'], unique=False)


def downgrade():
  op.drop_index('fk_risks_secondary_contact', table_name='risks')
  op.drop_column('risks', 'secondary_contact_id')
  op.drop_index('fk_risk_objects_secondary_contact', table_name='risk_objects')
  op.drop_column('risk_objects', 'secondary_contact_id')
  op.drop_index('fk_threat_actors_secondary_contact', table_name='threat_actors')
  op.drop_column('threat_actors', 'secondary_contact_id')
