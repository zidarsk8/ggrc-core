
"""constrains object owners

Revision ID: 4ceda387a468
Revises: 5254f4f31427
Create Date: 2015-03-11 10:27:38.623654

"""

# revision identifiers, used by Alembic.
revision = '4ceda387a468'
down_revision = '5254f4f31427'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('set session old_alter_table=1; ALTER IGNORE TABLE object_owners ADD UNIQUE INDEX(person_id, ownable_id, ownable_type);')
    op.create_unique_constraint('uq_id_owners', 'object_owners', ['person_id', 'ownable_id', 'ownable_type'])


def downgrade():
    op.drop_constraint('uq_id_owners', 'object_owners', 'unique')
