# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add some indexes

Revision ID: 46fe552ca250
Revises: 610e2ece282
Create Date: 2014-04-30 00:00:59.066197

"""

# revision identifiers, used by Alembic.
revision = '46fe552ca250'
down_revision = '610e2ece282'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('fk_audits_contact', 'audits', ['contact_id'], unique=False)
    op.create_index('fk_audits_contexts', 'audits', ['context_id'], unique=False)
    op.create_index('fk_contexts_contexts', 'contexts', ['context_id'], unique=False)
    op.create_index('fk_controls_contact', 'controls', ['contact_id'], unique=False)
    op.create_index('fk_data_assets_contact', 'data_assets', ['contact_id'], unique=False)
    op.create_index('fk_directive_controls_contexts', 'directive_controls', ['context_id'], unique=False)
    op.drop_index('ix_context_id', table_name='directive_controls')
    op.create_index('fk_directive_sections_contexts', 'directive_sections', ['context_id'], unique=False)
    op.create_index('fk_directives_contact', 'directives', ['contact_id'], unique=False)
    op.create_index('fk_facilities_contact', 'facilities', ['contact_id'], unique=False)
    op.create_index('fk_markets_contact', 'markets', ['contact_id'], unique=False)
    op.create_index('fk_meetings_contexts', 'meetings', ['context_id'], unique=False)
    op.create_index('fk_object_controls_contexts', 'object_controls', ['context_id'], unique=False)
    op.create_index('fk_object_objectives_contexts', 'object_objectives', ['context_id'], unique=False)
    op.create_index('fk_object_owners_contexts', 'object_owners', ['context_id'], unique=False)
    op.create_index('fk_object_sections_contexts', 'object_sections', ['context_id'], unique=False)
    op.create_index('fk_objective_controls_contexts', 'objective_controls', ['context_id'], unique=False)
    op.create_index('fk_objectives_contact', 'objectives', ['contact_id'], unique=False)
    op.create_index('fk_objectives_contexts', 'objectives', ['context_id'], unique=False)
    op.create_index('fk_org_groups_contact', 'org_groups', ['contact_id'], unique=False)
    op.create_index('fk_products_contact', 'products', ['contact_id'], unique=False)
    op.create_index('fk_program_controls_contexts', 'program_controls', ['context_id'], unique=False)
    op.create_index('fk_programs_contact', 'programs', ['contact_id'], unique=False)
    op.create_index('fk_projects_contact', 'projects', ['contact_id'], unique=False)
    op.create_index('fk_requests_contexts', 'requests', ['context_id'], unique=False)
    op.create_index('fk_responses_contact', 'responses', ['contact_id'], unique=False)
    op.create_index('fk_responses_contexts', 'responses', ['context_id'], unique=False)
    op.create_index('fk_section_objectives_contexts', 'section_objectives', ['context_id'], unique=False)
    op.create_index('fk_sections_contact', 'sections', ['contact_id'], unique=False)
    op.create_index('fk_systems_contact', 'systems', ['contact_id'], unique=False)
    op.create_index('fk_tasks_contexts', 'tasks', ['context_id'], unique=False)


def downgrade():
    op.drop_index('fk_tasks_contexts', table_name='tasks')
    op.drop_index('fk_systems_contact', table_name='systems')
    op.drop_index('fk_sections_contact', table_name='sections')
    op.drop_index('fk_section_objectives_contexts', table_name='section_objectives')
    op.drop_index('fk_responses_contexts', table_name='responses')
    op.drop_index('fk_responses_contact', table_name='responses')
    op.drop_index('fk_requests_contexts', table_name='requests')
    op.drop_index('fk_projects_contact', table_name='projects')
    op.drop_index('fk_programs_contact', table_name='programs')
    op.drop_index('fk_program_controls_contexts', table_name='program_controls')
    op.drop_index('fk_products_contact', table_name='products')
    op.drop_index('fk_org_groups_contact', table_name='org_groups')
    op.drop_index('fk_objectives_contexts', table_name='objectives')
    op.drop_index('fk_objectives_contact', table_name='objectives')
    op.drop_index('fk_objective_controls_contexts', table_name='objective_controls')
    op.drop_index('fk_object_sections_contexts', table_name='object_sections')
    op.drop_index('fk_object_owners_contexts', table_name='object_owners')
    op.drop_index('fk_object_objectives_contexts', table_name='object_objectives')
    op.drop_index('fk_object_controls_contexts', table_name='object_controls')
    op.drop_index('fk_meetings_contexts', table_name='meetings')
    op.drop_index('fk_markets_contact', table_name='markets')
    op.drop_index('fk_facilities_contact', table_name='facilities')
    op.drop_index('fk_directives_contact', table_name='directives')
    op.drop_index('fk_directive_sections_contexts', table_name='directive_sections')
    op.create_index('ix_context_id', 'directive_controls', ['context_id'], unique=False)
    op.drop_index('fk_directive_controls_contexts', table_name='directive_controls')
    op.drop_index('fk_data_assets_contact', table_name='data_assets')
    op.drop_index('fk_controls_contact', table_name='controls')
    op.drop_index('fk_contexts_contexts', table_name='contexts')
    op.drop_index('fk_audits_contexts', table_name='audits')
    op.drop_index('fk_audits_contact', table_name='audits')
