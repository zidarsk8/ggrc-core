# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for workflow cycle calculator."""

from datetime import date

from ggrc import app  # noqa #pylint: disable=unused-import
from ggrc import db
from ggrc_workflows import models
from ggrc_workflows.services.workflow_cycle_calculator import cycle_calculator


from integration.ggrc_workflows.workflow_cycle_calculator \
    import base_workflow_test_case

# pylint: disable=invalid-name


class TestCycleCalculator(base_workflow_test_case.BaseWorkflowTestCase):

  def test_weekend_holiday_adjustment(self):
    """Test weekend adjustments

    CycleCalculator is an abstract class, a bit of black magic to fake
    calling abstract class.
    """
    weekly_wf = {
        "title": "weekly thingy",
        "description": "start this many a time",
        "frequency": "weekly",
        "task_groups": [{
            "title": "tg_2",
            "task_group_tasks": [
                {
                    'title': 'weekly task 1',
                    "relative_start_day": 2,  # Tuesday, 9th
                    "relative_start_month": None,
                    "relative_end_day": 4,  # Thursday, 11th
                    "relative_end_month": None,
                }
            ],
            "task_group_objects": self.random_objects
        },
        ]
    }
    _, wf = self.generator.generate_workflow(weekly_wf)
    self.generator.generate_task_group(wf)
    self.generator.activate_workflow(wf)
    active_wf = db.session.query(models.Workflow).filter(
        models.Workflow.id == wf.id).one()

    cycle_calculator.CycleCalculator.__abstractmethods__ = set()
    cycle_calculator.CycleCalculator.get_relative_start = \
        lambda self, task: 4  # RFC 1149.5
    calc = cycle_calculator.CycleCalculator(active_wf)  # noqa # pylint: disable=abstract-class-instantiated

    # Check if weekend adjustments work
    self.assertEqual(calc.adjust_date(date(2015, 6, 20)), date(2015, 6, 19))
    self.assertEqual(calc.adjust_date(date(2015, 6, 21)), date(2015, 6, 19))

    # Check if holiday adjustments across the years work
    self.assertEqual(calc.adjust_date(date(2015, 1, 1)), date(2014, 12, 30))

    # Check if holiday + weekend adjustments work
    calc.holidays = [date(2015, 6, 24), date(2015, 6, 25), date(2015, 6, 26)]
    self.assertEqual(calc.adjust_date(date(2015, 6, 28)), date(2015, 6, 23))
