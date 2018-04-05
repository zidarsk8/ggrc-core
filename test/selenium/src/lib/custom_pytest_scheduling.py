# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Custom Pytest schedulers"""

from xdist.scheduler import LoadScheduling

from lib.constants.test_runner import DESTRUCTIVE_TEST_METHOD_PREFIX


class CustomPytestScheduling(LoadScheduling):
  """Pytest scheduler.
  The only difference from LoadScheduling is that it sends all "destructive"
  tests to the same node. It is done so they will not collide with other tests
  running in parallel.
  A test is marked as destructive by starting its name with "test_destructive".
  """

  def _send_tests(self, node, num):
    idxs_to_send = []
    for idx, test_name in enumerate(self.collection):
      if self._is_destructive_test(test_name) and idx in self.pending:
        idxs_to_send.append(idx)
    if not idxs_to_send:
      idxs_to_send = self.pending[:num]
    self._execute_tests(node, idxs_to_send)

  def _execute_tests(self, node, idxs_to_send):
    """Run tests represented by `idxs_to_send` at `node`"""
    for test_idx in idxs_to_send:
      self.pending.remove(test_idx)
    self.node2pending[node].extend(idxs_to_send)
    node.send_runtest_some(idxs_to_send)

  @staticmethod
  def _is_destructive_test(test_id):
    return DESTRUCTIVE_TEST_METHOD_PREFIX in test_id
