# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com
from __future__ import absolute_import

import ggrc
import ggrc.settings
import os
import sys

def main():
  import behave.runner

  class GGRCRunner(behave.runner.Runner):
    def path_in_args(self, path):
      for arg in sys.argv:
        if not arg.startswith('-') and \
            os.path.abspath(arg) == path:
          return True
      return False

    def get_ggrc_base_path(self):
      return os.path.join(
          os.path.abspath(os.path.dirname(os.path.dirname(ggrc.__file__))),
          'service_specs')

    def get_ggrc_steps_path(self):
      base_dir = self.get_ggrc_base_path()
      if self.path_in_args(base_dir):
        return None
      # add to sys.path so that the utils and other test helper modules can
      # be found
      path = os.path.join(base_dir, 'steps')
      sys.path.append(path)
      print 'sys.path', sys.path
      return path

    def load_step_definitions(self, extra_step_paths=[]):
      # Ensure that src/service_specs/steps is in step paths
      ggrc_steps_path = self.get_ggrc_steps_path()
      if ggrc_steps_path is not None \
          and ggrc_steps_path != os.path.join(self.base_dir, 'steps'):
        extra_step_paths = list(extra_step_paths)
        extra_step_paths.append(ggrc_steps_path)
      print 'extra_step_paths', extra_step_paths
      super(GGRCRunner, self).load_step_definitions(
          extra_step_paths=extra_step_paths)

    def load_hooks(self, filename=None):
      filename = filename or \
          os.path.join(self.get_ggrc_base_path(), 'environment.py')
      return super(GGRCRunner, self).load_hooks(filename=filename)

  import behave.__main__
  # Patching the Runner class to use the modified GGRCRunner
  behave.__main__.Runner = GGRCRunner
  ret = behave.__main__.main()
  # Put things back as they were, just for general hygiene's sake
  behave.__main__.Runner = behave.runner.Runner
  return ret

if __name__ == '__main__':
  main()

