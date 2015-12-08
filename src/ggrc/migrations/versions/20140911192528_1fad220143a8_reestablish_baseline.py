# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Reestablish baseline

Revision ID: 1fad220143a8
Revises: 19abed0bcf16
Create Date: 2014-09-11 19:25:28.836977

"""

# revision identifiers, used by Alembic.
revision = '1fad220143a8'
down_revision = '19abed0bcf16'

from alembic import op


def upgrade():
    op.create_index('fk_background_tasks_contexts', 'background_tasks', ['context_id'], unique=False)
    op.drop_index('fk_tasks_contexts', table_name='background_tasks')
    op.create_index('fk_calendar_entries_contexts', 'calendar_entries', ['context_id'], unique=False)
    op.create_index('fk_notification_configs_contexts', 'notification_configs', ['context_id'], unique=False)
    op.create_index('fk_notification_objects_contexts', 'notification_objects', ['context_id'], unique=False)
    op.create_index('fk_notification_recipients_contexts', 'notification_recipients', ['context_id'], unique=False)
    op.create_index('fk_notifications_contexts', 'notifications', ['context_id'], unique=False)


def downgrade():
    op.drop_index('fk_notifications_contexts', table_name='notifications')
    op.drop_index('fk_notification_recipients_contexts', table_name='notification_recipients')
    op.drop_index('fk_notification_objects_contexts', table_name='notification_objects')
    op.drop_index('fk_notification_configs_contexts', table_name='notification_configs')
    op.drop_index('fk_calendar_entries_contexts', table_name='calendar_entries')
    op.create_index('fk_tasks_contexts', 'background_tasks', ['context_id'], unique=False)
    op.drop_index('fk_background_tasks_contexts', table_name='background_tasks')
