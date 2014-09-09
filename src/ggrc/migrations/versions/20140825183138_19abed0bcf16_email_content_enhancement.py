
"""email_content_enhancement

Revision ID: 19abed0bcf16
Revises: 5509cd84a758
Create Date: 2014-08-25 18:31:38.211566

"""

# revision identifiers, used by Alembic.
revision = '19abed0bcf16'
down_revision = '10bf713673f8'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('notification_recipients', sa.Column('content', sa.Text(), nullable=True))

def downgrade():
  op.drop_column('notification_recipients', 'content')
