# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test issue_tracker hooks."""

import unittest

import ddt
import mock

from ggrc.models.hooks.issue_tracker import assessment_integration
from ggrc.models.hooks.issue_tracker import integration_utils


@ddt.ddt
class TestUtilityFunctions(unittest.TestCase):
  """Test utility function in issue_tracker module."""

  def setUp(self):
    super(TestUtilityFunctions, self).setUp()
    self.session = mock.MagicMock()

  @ddt.data(
      (
          {
              'component_id': '1111',
              'hotlist_id': '2222',
              'issue_type': 'PROCESS',
              'issue_priority': 'P2',
              'issue_severity': 'S2',
              'title': 'Title'
          },
          None
      ),
      (
          {
              'component_id': '1111',
              'hotlist_id': '2222',
              'issue_type': 'PROCESS',
              'issue_priority': 'P2',
              'issue_severity': 'S2',
              'title': 'Title'
          },
          None,
      ),
      (
          {
              'component_id': '1111',
              'hotlist_id': '2222',
              'issue_type': 'PROCESS',
              'issue_priority': 'P2',
              'issue_severity': 'S2',
              'title': 'Title'
          },
          None,
      ),
      (
          {
              'component_id': 'zzz',
              'hotlist_id': '2222',
              'issue_type': 'PROCESS',
              'issue_priority': 'P2',
              'issue_severity': 'S2',
              'title': 'Title'
          },
          integration_utils.exceptions.ValidationError,),
      (
          {
              'component_id': '11111',
              'hotlist_id': 'zzz',
              'issue_type': 'PROCESS',
              'issue_priority': 'P2',
              'issue_severity': 'S2',
              'title': 'Title'
          },
          integration_utils.exceptions.ValidationError,),
  )
  @ddt.unpack
  def test_validate_info(self, info, expected_error):
    """Test _validate_issue_tracker_info function."""
    initial_info = dict(info)
    tracker_handler = assessment_integration.AssessmentTrackerHandler()
    # pylint: disable=protected-access
    if expected_error:
      with self.assertRaises(expected_error):
        tracker_handler._validate_generic_fields(info)
    else:
      tracker_handler._validate_generic_fields(info)

    self.assertEqual(info, initial_info)

  @ddt.data(
      ({'component_id': '1111', 'hotlist_id': '2222'},
       {'component_id': 1111, 'hotlist_id': 2222},
       None,),
      ({'component_id': '1111'},
       {'component_id': 1111},
       None,),
      ({'hotlist_id': '2222'},
       {'hotlist_id': 2222},
       None,),
      ({'component_id': 'zzz'},
       None,
       integration_utils.exceptions.ValidationError,),
      ({'hotlist_id': 'zzz'},
       None,
       integration_utils.exceptions.ValidationError,),
  )
  @ddt.unpack
  def test_normalize_info(self, info, expected, expected_error):
    """Test _normalize_issue_tracker_info function."""
    # pylint: disable=protected-access
    if expected_error:
      with self.assertRaises(expected_error):
        integration_utils.normalize_issue_tracker_info(info)
    else:
      integration_utils.normalize_issue_tracker_info(info)
      self.assertEqual(info, expected)

  @ddt.data(
      ([], [], []),
      (["1@e.w", "1@e.w"], ["1@e.w", "2@e.w"], ["1@e.w", "2@e.w"]),
      (["1@e.w", "2@e.w"], ["3@e.w", "2@e.w"], ["1@e.w", "2@e.w", "3@e.w"]),
      (["1@e.w", "2@e.w"],
       ["3@e.w", "4@e.w"],
       ["1@e.w", "2@e.w", "3@e.w", "4@e.w"]),
  )
  @ddt.unpack
  def test_merge_ccs_method(self, object_ccs, additional_ccs, expected_ccs):
    """Test merge_ccs method"""
    # pylint: disable=protected-access
    tracker_handler = assessment_integration.AssessmentTrackerHandler()
    grouped_ccs = tracker_handler._merge_ccs(
        object_ccs,
        additional_ccs,
    )
    self.assertEqual(set(grouped_ccs), set(expected_ccs))

  def test_reporter_sync_exists(self):
    """Test for get reporter on sync if reporter exists."""
    # pylint: disable=protected-access
    mock_object = mock.MagicMock(id=1)
    with mock.patch.object(
        assessment_integration.AssessmentTrackerHandler,
        '_is_reporter_exists',
        return_value=True
    ):
      tracker_handler = assessment_integration.AssessmentTrackerHandler()
      reporter = "reporter@test.com"
      reporter_tracker = tracker_handler._get_reporter_on_sync(
          mock_object,
          reporter
      )
      self.assertEqual(reporter, reporter_tracker)

  @mock.patch.object(
      assessment_integration.AssessmentTrackerHandler,
      '_get_reporter',
      lambda obj, audit_id: "repoter2@test.com"
  )
  def test_reporter_sync_not_exists(self):
    """Test for get reporter on sync if not exists."""
    # pylint: disable=protected-access
    mock_object = mock.MagicMock(id=1)
    with mock.patch.object(
        assessment_integration.AssessmentTrackerHandler,
        '_is_reporter_exists',
        return_value=False
    ):
      tracker_handler = assessment_integration.AssessmentTrackerHandler()
      reporter = "reporter@test.com"
      reporter_tracker = tracker_handler._get_reporter_on_sync(
          audit=mock_object,
          reporter_db=reporter
      )
      self.assertEqual(
          "repoter2@test.com",
          reporter_tracker
      )

  def test_assignee_sync_exists(self):
    """Test for get assignee on sync if assignee exists."""
    # pylint: disable=protected-access
    assmt_object = mock.MagicMock(id=1)
    with mock.patch.object(
        assessment_integration.AssessmentTrackerHandler,
        '_is_assignee_exists',
        return_value=True
    ):
      tracker_handler = assessment_integration.AssessmentTrackerHandler()
      assignee = "assignee@test.com"
      assignee_tracker = tracker_handler._get_assignee_on_sync(
          assmt_object,
          assignee
      )
      self.assertEqual(assignee, assignee_tracker)

  @mock.patch.object(
      assessment_integration.AssessmentTrackerHandler,
      '_get_assignee',
      lambda obj, assmt_id: "assignee2@test.com"
  )
  def test_assignee_sync_not_exists(self):
    """Test for get assignee on sync if not assignee exists."""
    # pylint: disable=protected-access
    assmt_object = mock.MagicMock(id=1)
    with mock.patch.object(
        assessment_integration.AssessmentTrackerHandler,
        '_is_assignee_exists',
        return_value=False
    ):
      tracker_handler = assessment_integration.AssessmentTrackerHandler()
      reporter = "assignee@test.com"
      reporter_tracker = tracker_handler._get_assignee_on_sync(
          assmt_object,
          reporter
      )
      self.assertEqual(
          "assignee2@test.com",
          reporter_tracker
      )
