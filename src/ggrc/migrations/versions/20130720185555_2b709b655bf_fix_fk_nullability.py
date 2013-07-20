"""Fix fk nullability

Revision ID: 2b709b655bf
Revises: 1b4c52e33cc6
Create Date: 2013-07-20 18:55:55.285595

"""

# revision identifiers, used by Alembic.
revision = '2b709b655bf'
down_revision = '1b4c52e33cc6'

from alembic import op
import sqlalchemy as sa

NOT_NULL_COLS = [('control_risks', 'control_id'),
                     ('control_risks', 'risk_id'),
                     ('categorizations', 'category_id'),
                     ('control_assessments', 'pbc_list_id'),
                     ('control_assessments', 'control_id'),
                     ('control_controls', 'control_id'),
                     ('control_controls', 'implemented_control_id'),
                     ('control_sections', 'control_id'),
                     ('control_sections', 'section_id'),
                     ('cycles', 'program_id'),
                     ('meetings', 'response_id'),
                     ('object_documents', 'document_id'),
                     ('object_people', 'person_id'),
                     ('pbc_lists', 'audit_cycle_id'),
                     ('population_samples', 'response_id'),
                     ('program_directives', 'program_id'),
                     ('program_directives', 'directive_id'),
                     ('requests', 'pbc_list_id'),
                     ('responses', 'request_id'),
                     ('responses', 'system_id'),
                     ('risk_risky_attributes', 'risk_id'),
                     ('risk_risky_attributes', 'risky_attribute_id'),
                     ('sections', 'directive_id'),
                     ('system_controls', 'system_id'),
                     ('system_controls', 'control_id'),
                     ('system_systems', 'parent_id'),
                     ('system_systems', 'child_id'),
]

EXPLICIT_INDEXES = [('control_risks', 'control_id', 'controls', 'control_risks_ibfk_1'),
                    ('control_risks', 'risk_id', 'risks', 'control_risks_ibfk_2'),
                    ('control_assessments', 'control_id', 'controls', 'control_assessments_ibfk_1'),
                    ('control_assessments', 'pbc_list_id', 'pbc_lists', 'control_assessments_ibfk_2'),
                    ('control_controls', 'control_id', 'controls', 'control_controls_ibfk_1'),
                    ('control_controls', 'implemented_control_id', 'controls', 'control_controls_ibfk_2'),
                    ('control_sections', 'control_id', 'controls', 'control_sections_ibfk_1'),
                    ('control_sections', 'section_id', 'sections', 'control_sections_ibfk_2'),
                    ('program_directives', 'directive_id', 'directives', 'program_directives_ibfk_1'),
                    ('program_directives', 'program_id', 'programs', 'program_directives_ibfk_2'),
                    ('responses', 'request_id', 'requests', 'responses_ibfk_1'),
                    ('responses', 'system_id', 'systems', 'responses_ibfk_2'),
                    ('risk_risky_attributes', 'risk_id', 'risks', 'risk_risky_attributes_ibfk_1'),
                    ('risk_risky_attributes', 'risky_attribute_id', 'risky_attributes', 'risk_risky_attributes_ibfk_2'),
                    ('system_controls', 'system_id', 'systems', 'system_controls_ibfk_3'),
                    ('system_controls', 'control_id', 'controls', 'system_controls_ibfk_1'),
                    ('system_systems', 'child_id', 'systems', 'system_systems_ibfk_1'),
                    ('system_systems', 'parent_id', 'systems', 'system_systems_ibfk_2'),
]

UNIQUE_CONSTRAINTS = [('control_assessments', ['pbc_list_id', 'control_id']),
                      ('control_controls', ['control_id', 'implemented_control_id']),
                      ('control_risks', ['control_id', 'risk_id']),
                      ('control_sections', ['control_id', 'section_id']),
                      ('program_directives', ['program_id', 'directive_id']),
                      ('responses', ['request_id', 'system_id']),
                      ('risk_risky_attributes', ['risk_id', 'risky_attribute_id']),
                      ('system_controls', ['system_id', 'control_id']),
                      ('system_systems', ['parent_id', 'child_id']),
]

def create_explicit_index(table, column, referred_table, constraint_name):
    " Explicit indexes need to be created to work around http://bugs.mysql.com/bug.php?id=21395 "
    op.drop_constraint(constraint_name, table, type_='foreignkey')
    op.create_index('ix_' + column, table, [column])
    op.create_foreign_key(constraint_name, table, referred_table, [column], ['id'])

def drop_explicit_index(table, column, referred_table, constraint_name):
    op.drop_constraint(constraint_name, table, type_='foreignkey')
    op.drop_index('ix_' + column, table)
    op.create_foreign_key(constraint_name, table, referred_table, [column], ['id'])

def upgrade():
    for table, column in NOT_NULL_COLS:
        op.alter_column(table, column, nullable=False, existing_type = sa.INTEGER)
    for table, column, referred_table, constraint_name in EXPLICIT_INDEXES:
        create_explicit_index(table, column, referred_table, constraint_name) 
    for table, columns in UNIQUE_CONSTRAINTS:
        op.create_unique_constraint('uq_' + table, table, columns)


def downgrade():
    for table, columns in UNIQUE_CONSTRAINTS:
        op.drop_constraint('uq_' + table, table, type_='unique')
    for table, column, referred_table, constraint_name in EXPLICIT_INDEXES:
        drop_explicit_index(table, column, referred_table, constraint_name) 
    for table, column in NOT_NULL_COLS:
        op.alter_column(table, column, nullable=True, existing_type = sa.INTEGER)
