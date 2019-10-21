# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Mega program tests."""
# pylint: disable=no-self-use


from lib import base
from lib.service import webui_facade


class TestMegaProgram(base.Test):
  """Tests for mega program feature."""

  def test_techenv_mapped_to_programs(
      self, programs_with_audit_and_techenv, selenium, soft_assert
  ):
    """ Check if Technology Environment is mapped to
        both program 1 and 2.
        Objects structure:
          Program 1
          -> Program 2
            -> Audit
              -> Technology Environment
        Preconditions:
        - Programs, Technology Environment created via REST API.
    """
    webui_facade.soft_assert_techenv_mapped_to_programs(
        programs_with_audit_and_techenv, selenium, soft_assert)
    soft_assert.assert_expectations()
