# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


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
    op.execute('delete from object_owners where id in (select id from (select id, count(id) as count from object_owners group by person_id, ownable_id, ownable_type having count > 1) as c );')
    op.create_unique_constraint('uq_id_owners', 'object_owners', ['person_id', 'ownable_id', 'ownable_type'])


def downgrade():
    op.drop_constraint('uq_id_owners', 'object_owners', 'unique')
