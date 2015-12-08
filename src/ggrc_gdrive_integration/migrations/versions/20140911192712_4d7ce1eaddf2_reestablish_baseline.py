# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Reestablish baseline

Revision ID: 4d7ce1eaddf2
Revises: 4a72628695ff
Create Date: 2014-09-11 19:27:12.187443

"""

# revision identifiers, used by Alembic.
revision = '4d7ce1eaddf2'
down_revision = '4a72628695ff'

from alembic import op


def upgrade():
    op.create_index('fk_object_events_contexts', 'object_events', ['context_id'], unique=False)
    op.create_index('fk_object_files_contexts', 'object_files', ['context_id'], unique=False)
    op.create_index('fk_object_folders_contexts', 'object_folders', ['context_id'], unique=False)


def downgrade():
    op.drop_index('fk_object_folders_contexts', table_name='object_folders')
    op.drop_index('fk_object_files_contexts', table_name='object_files')
    op.drop_index('fk_object_events_contexts', table_name='object_events')
