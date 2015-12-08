# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from blinker import Namespace

class Signals():
  signals = Namespace()
  status_change = signals.signal(
      'Status Changed',
      """
    This is used to signal any listeners of any changes in model object status
    attribute
    """)

  workflow_cycle_start = signals.signal(
      'Workflow Cycle Started ',
      """
    This is used to signal any listeners of any workflow cycle start
    attribute
    """)
