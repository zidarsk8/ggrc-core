# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Initialize GGRC Workflow related models' hooks."""
from ggrc_workflows.models.hooks import workflow


ALL_HOOKS = (workflow,)


def init_hooks():
  """Initialize Workflow related models' hooks."""
  for hook in ALL_HOOKS:
    hook.init_hook()
