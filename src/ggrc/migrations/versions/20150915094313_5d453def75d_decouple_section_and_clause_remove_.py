
"""Decouple section and clause, remove directive foreign key

Revision ID: 5d453def75d
Revises: 2d8a46b1e4a4
Create Date: 2015-09-15 09:43:13.781166

"""

# revision identifiers, used by Alembic.
revision = '5d453def75d'
down_revision = '2d8a46b1e4a4'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.create_table('clauses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=250), nullable=True),
    sa.Column('na', sa.Boolean(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('os_state', sa.String(length=250), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.Column('reference_url', sa.String(length=250), nullable=True),
    sa.Column('secondary_contact_id', sa.Integer(), nullable=True),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('slug', sa.String(length=250), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('context_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=250), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['clauses.id'], ),
    sa.ForeignKeyConstraint(['secondary_contact_id'], ['people.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug', name='uq_clauses')
    )

    op.drop_column('sections', 'directive_id')


def downgrade():
    op.add_column('sections', sa.Column('directive_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))

    op.drop_table('clauses')
