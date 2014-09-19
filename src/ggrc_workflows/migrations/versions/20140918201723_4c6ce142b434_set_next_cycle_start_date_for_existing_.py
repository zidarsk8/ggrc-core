"""set next cycle start date for existing workflows

Revision ID: 4c6ce142b434
Revises: 53dcddf6c09e
Create Date: 2014-09-18 20:17:23.080878

"""

# revision identifiers, used by Alembic.
revision = '4c6ce142b434'
down_revision = '53dcddf6c09e'

from datetime import date
from ggrc import settings, db
from alembic import op
import sqlalchemy as sa
import ggrc_workflows.models as models
from ggrc_workflows.models import *
from ggrc_workflows.models.mixins import RelativeTimeboxed

def upgrade():
  
  today = date.today()
  
  # Get all active workflows with no next_cycle_start_date
  workflows = db.session.query(models.Workflow)\
    .filter(
        models.Workflow.next_cycle_start_date == None,
        models.Workflow.recurrences == True,
        models.Workflow.status == 'Active'
        ).all()
  
  # Update all workflows.
  for workflow in workflows:
    base_date = RelativeTimeboxed._calc_base_date(today, workflow.frequency)
    next_date = RelativeTimeboxed._calc_start_date_of_next_period(base_date, workflow.frequency)
    workflow.next_cycle_start_date = next_date
    db.session.add(workflow)

  # Save
  db.session.commit()

def downgrade():
    pass
