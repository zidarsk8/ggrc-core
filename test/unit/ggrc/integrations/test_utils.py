# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit tests for client module."""
# pylint: disable=protected-access

import unittest

import mock

from ggrc.integrations import integrations_errors
from ggrc.integrations import utils


class BaseClientTest(unittest.TestCase):
  """Tests basic functions."""

  def test_collect_assessment_issues(self):
    """Tests collection issues associated with Assessments."""
    assessment1_mock = mock.MagicMock(id=1, status='In Review')
    assessment2_mock = mock.MagicMock(id=2, status='WRONG STATUS')
    issue1_mock = mock.MagicMock(
        issue_tracked_obj=assessment1_mock,
        issue_id='t1',
        issue_type='bug1',
        issue_priority='P1',
        issue_severity='S1')
    issue2_mock = mock.MagicMock(
        issue_tracked_obj=assessment2_mock,
        issue_id='t2',
        issue_type='bug2',
        issue_priority='P2',
        issue_severity='S2')
    issue3_mock = mock.MagicMock(
        issue_tracked_obj=None,
        issue_id='t3',
        issue_type='bug3',
        issue_priority='P3',
        issue_severity='S3')
    filter_mock = mock.MagicMock()
    filter_mock.return_value.order_by.return_value.all.return_value = [
        issue1_mock,
        issue2_mock,
        issue3_mock,
    ]
    with mock.patch.multiple(
        utils.models.IssuetrackerIssue,
        query=mock.MagicMock(filter=filter_mock)
    ):
      actual = utils._collect_assessment_issues()
      self.assertEquals(actual, {
          't1': {
              'assessment_id': 1,
              'state': {
                  'status': 'FIXED',
                  'type': 'bug1',
                  'priority': 'P1',
                  'severity': 'S1',
              },
          }
      })

  def test_iter_issue_batches(self):
    """Tests fetching issues from Issue Tracer in batches."""
    cli_mock = mock.MagicMock()
    cli_mock.search.side_effect = iter([
        {
            'issues': [
                {
                    'issueId': 't1',
                    'issueState': {
                        'status': 'FIXED',
                        'type': 'bug1',
                        'priority': 'P1',
                        'severity': 'S1',
                    },
                },
                {
                    'issueId': 't2',
                    'issueState': {
                        'status': 'FIXED',
                        'type': 'bug2',
                        'priority': 'P2',
                        'severity': 'S2',
                    },
                },
            ],
            'next_page_token': 'token1',
        },
        {
            'issues': [],
            'next_page_token': 'token2',
        },
        {
            'issues': [
                {
                    'issueId': 't3',
                    'issueState': {
                        'status': 'FIXED',
                        'type': 'bug3',
                        'priority': 'P3',
                        'severity': 'S3',
                    },
                },
            ],
            'next_page_token': None,
        },
    ])
    with mock.patch.object(utils.issues, 'Client', return_value=cli_mock):
      actual = list(utils._iter_issue_batches([1, 2, 3]))
      self.assertEquals(actual, [
          {
              't1': {
                  'status': 'FIXED',
                  'type': 'bug1',
                  'priority': 'P1',
                  'severity': 'S1',
              },
              't2': {
                  'status': 'FIXED',
                  'type': 'bug2',
                  'priority': 'P2',
                  'severity': 'S2',
              },
          },
          {
              't3': {
                  'status': 'FIXED',
                  'type': 'bug3',
                  'priority': 'P3',
                  'severity': 'S3',
              },
          },
      ])
      self.assertEqual(cli_mock.search.call_args_list, [
          mock.call({
              'issue_ids': [1, 2, 3],
              'page_size': 100,
              'page_token': None,
          }),
          mock.call({
              'issue_ids': [1, 2, 3],
              'page_size': 100,
              'page_token': 'token1',
          }),
          mock.call({
              'issue_ids': [1, 2, 3],
              'page_size': 100,
              'page_token': 'token2',
          }),
      ])

  def test_iter_issue_batches_error(self):
    """Tests handling error fetching issues from Issue Tracer in batches."""
    cli_mock = mock.MagicMock()
    cli_mock.search.side_effect = integrations_errors.HttpError('Test')
    with mock.patch.object(utils.issues, 'Client', return_value=cli_mock):
      actual = list(utils._iter_issue_batches([1, 2, 3]))
      self.assertEqual(actual, [])

  def test_update_issue(self):
    """Tests updating issue."""
    cli_mock = mock.MagicMock()
    self.assertIsNone(utils._update_issue(cli_mock, 1, 'params'))
    cli_mock.update_issue.assert_called_once_with(1, 'params')

  def test_update_issue_with_retry(self):
    """Tests updating issue with retry."""
    cli_mock = mock.MagicMock()
    exception = integrations_errors.HttpError('Test', status=429)
    cli_mock.update_issue.side_effect = iter([
        exception,
        exception,
        exception,
        exception,
        None,
    ])
    with mock.patch.object(utils.time, 'sleep') as sleep_mock:
      utils._update_issue(cli_mock, 1, 'params')
      self.assertEqual(cli_mock.update_issue.call_args_list, [
          mock.call(1, 'params'),
          mock.call(1, 'params'),
          mock.call(1, 'params'),
          mock.call(1, 'params'),
          mock.call(1, 'params'),
      ])
      self.assertEqual(sleep_mock.call_args_list, [
          mock.call(1),
          mock.call(1),
          mock.call(1),
          mock.call(1),
      ])

  def test_update_issue_with_raise(self):
    """Tests updating issue with raising an exception."""
    cli_mock = mock.MagicMock()
    exception = integrations_errors.HttpError('Test', status=429)
    cli_mock.update_issue.side_effect = iter([
        exception,
        exception,
        exception,
        exception,
        exception,
    ])
    with mock.patch.object(utils.time, 'sleep') as sleep_mock:
      with self.assertRaises(integrations_errors.HttpError) as exc_mock:
        utils._update_issue(cli_mock, 1, 'params')
        self.assertEqual(exc_mock.exception.status, 429)
        self.assertEqual(cli_mock.update_issue.call_args_list, [
            mock.call(1, 'params'),
            mock.call(1, 'params'),
            mock.call(1, 'params'),
            mock.call(1, 'params'),
            mock.call(1, 'params'),
        ])
        self.assertEqual(sleep_mock.call_args_list, [
            mock.call(1),
            mock.call(1),
            mock.call(1),
            mock.call(1),
        ])

  def test_sync_issue_tracker_statuses(self):  # pylint: disable=invalid-name
    """Tests issue synchronization flow."""
    assessment_issues = {
        't1': {
            'assessment_id': 1,
            'state': {
                'status': 'FIXED',
                'type': 'BUG1',
                'priority': 'P1',
                'severity': 'S1',
            },
        },
        't2': {
            'assessment_id': 2,
            'state': {
                'status': 'ASSIGNED',
                'type': 'BUG2',
                'priority': 'P2',
                'severity': 'S2',
            },
        },
    }
    batches = [
        {
            't1': {
                'status': 'FIXED',
                'type': 'BUG1',
                'priority': 'P1',
                'severity': 'S1',
            },
        },
        {
            't2': {
                'status': 'FIXED',
                'type': 'BUG2',
                'priority': 'P2',
                'severity': 'S2',
            },
            'unexpected_issue': {
                'status': 'FIXED',
                'type': 'BUG2',
                'priority': 'P2',
                'severity': 'S2',
            },
        },
    ]

    cli_mock = mock.MagicMock()
    cli_patch = mock.patch.object(
        utils.issues, 'Client', return_value=cli_mock)

    with cli_patch, mock.patch.multiple(
        utils,
        _collect_assessment_issues=mock.MagicMock(
            return_value=assessment_issues),
        _iter_issue_batches=mock.MagicMock(
            return_value=iter(batches)),
        _update_issue=mock.DEFAULT
    ):
      utils.sync_issue_tracker_statuses()
      iter_calls = utils._iter_issue_batches.call_args_list
      self.assertEqual(len(iter_calls), 1)
      self.assertItemsEqual(iter_calls[0][0][0], ['t1', 't2'])
      utils._update_issue.assert_called_once_with(cli_mock, 't2', {
          'status': 'ASSIGNED',
          'type': 'BUG2',
          'priority': 'P2',
          'severity': 'S2',
      })
