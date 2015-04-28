
"""Remove ProgramDirective table

Revision ID: 3be12e136921
Revises: 57cc398ad417
Create Date: 2015-04-28 15:23:10.503624

"""

# revision identifiers, used by Alembic.
revision = '3be12e136921'
down_revision = '57cc398ad417'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
  sql = """
  INSERT INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT pd.modified_by_id, pd.created_at, pd.updated_at, pd.program_id as source_id,
         'Program' as source_type, pd.directive_id, IFNULL(d.kind,"Policy") as destination_type, pd.context_id
  FROM program_directives as pd JOIN directives as d ON pd.directive_id = d.id;
  """
  op.execute(sql)


def downgrade():
  pass
