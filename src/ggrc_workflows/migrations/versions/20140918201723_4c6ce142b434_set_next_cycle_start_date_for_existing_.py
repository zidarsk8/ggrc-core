# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

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

  from ggrc_workflows.services.workflow_cycle_calculator import get_cycle_calculator
  # Update all workflows.
  for workflow in workflows:
    base_date = date.today()
    calculator = get_cycle_calculator(workflow)
    workflow.next_cycle_start_date = \
      calculator.nearest_start_date_after_basedate(base_date)
    db.session.add(workflow)

  # Save
  db.session.commit()

def downgrade():
    pass
