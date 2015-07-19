# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Clean responses mapped to responses

Revision ID: 56bda17c92ee
Revises: 5308176a50c7
Create Date: 2015-03-21 21:24:21.399235

"""

# revision identifiers, used by Alembic.
revision = '56bda17c92ee'
down_revision = '5308176a50c7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    response_types = "('DocumentationResponse', 'InterviewResponse', 'PopulationSampleResponse')"

    op.execute("delete from relationships where source_type in "+response_types+" and destination_type in "+response_types)


def downgrade():
    pass
