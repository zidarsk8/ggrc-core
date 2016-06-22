# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Index for object_folders

Revision ID: 1efacad0fff5
Revises: 4d7ce1eaddf2
Create Date: 2014-09-12 21:11:35.908034

"""

# revision identifiers, used by Alembic.
revision = '1efacad0fff5'
down_revision = '4d7ce1eaddf2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ix_folderable_id_type', 'object_folders', ['folderable_type','folderable_id'])
    pass


def downgrade():
    op.drop_index('ix_folderable_id_type', table_name='object_folders')
    pass
