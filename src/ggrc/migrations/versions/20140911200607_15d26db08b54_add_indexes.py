# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add indexes

Revision ID: 15d26db08b54
Revises: 1fad220143a8
Create Date: 2014-09-11 20:06:07.580817

"""

# revision identifiers, used by Alembic.
revision = '15d26db08b54'
down_revision = '1fad220143a8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('ix_context_related_object', 'contexts', ['related_object_type', 'related_object_id'], unique=False)
    op.create_index('ix_directives_meta_kind', 'directives', ['meta_kind'], unique=False)
    op.create_index('ix_fulltext_record_properties_context_id', 'fulltext_record_properties', ['context_id'], unique=False)
    op.create_index('ix_fulltext_record_properties_key', 'fulltext_record_properties', ['key'], unique=False)
    op.create_index('ix_fulltext_record_properties_tags', 'fulltext_record_properties', ['tags'], unique=False)
    op.create_index('ix_fulltext_record_properties_type', 'fulltext_record_properties', ['type'], unique=False)
    op.create_index('ix_object_objectives_objectiveable', 'object_objectives', ['objectiveable_type', 'objectiveable_id'], unique=False)
    op.create_index('ix_object_owners_ownable', 'object_owners', ['ownable_type', 'ownable_id'], unique=False)
    op.create_index('ix_options_role', 'options', ['role'], unique=False)
    op.create_index('ix_relationships_destination', 'relationships', ['destination_type', 'destination_id'], unique=False)
    op.create_index('ix_relationships_source', 'relationships', ['source_type', 'source_id'], unique=False)
    op.create_index('ix_systems_is_biz_process', 'systems', ['is_biz_process'], unique=False)


def downgrade():
    op.drop_index('ix_systems_is_biz_process', table_name='systems')
    op.drop_index('ix_relationships_source', table_name='relationships')
    op.drop_index('ix_relationships_destination', table_name='relationships')
    op.drop_index('ix_options_role', table_name='options')
    op.drop_index('ix_object_owners_ownable', table_name='object_owners')
    op.drop_index('ix_object_objectives_objectiveable', table_name='object_objectives')
    op.drop_index('ix_fulltext_record_properties_type', table_name='fulltext_record_properties')
    op.drop_index('ix_fulltext_record_properties_tags', table_name='fulltext_record_properties')
    op.drop_index('ix_fulltext_record_properties_key', table_name='fulltext_record_properties')
    op.drop_index('ix_fulltext_record_properties_context_id', table_name='fulltext_record_properties')
    op.drop_index('ix_directives_meta_kind', table_name='directives')
    op.drop_index('ix_context_related_object', table_name='contexts')
