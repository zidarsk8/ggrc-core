# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for workflow people imports."""
# pylint: disable=invalid-name

import collections
import string
import ddt

from ggrc_workflows.models.workflow import Workflow
from integration.ggrc import TestCase
from integration.ggrc.models import factories as ggrc_factories


@ddt.ddt
class TestWorkflowPeopleImport(TestCase):
  """Tests for workflow people imports."""

  def setUp(self):
    with ggrc_factories.single_commit():
      self.user_emails = [
          ggrc_factories.PersonFactory().email for _ in xrange(8)]
    self.wf_slug = ggrc_factories.random_str(chars=string.ascii_letters)
    self.wf_import_params = collections.OrderedDict([
        ("object_type", "Workflow"),
        ("code", self.wf_slug),
        ("title", "SomeTitle"),
        ("Need Verification", 'True')
    ])

  def _check_workflow_people(self, import_data, expected_data, is_success,
                             success_resp_action):
    """Import people list to workflow and compare with expected results.

    Args:
        import_data: Dictionary contains 2 lists.
            'admins': Test people data indexes who should get Admin role.
            'members': Test people data indexes who should get Member role.
        expected_data: Dictionary contains 2 lists.
            'admins': Test people data indexes who should get Admin role.
            'members': Test people data indexes who should get Member role.
        is_success: Shows is import was successful or not.
        success_resp_action: Action which was performed on imported item.
    """
    if import_data['members']:
      import_members = '\n'.join(
          self.user_emails[idx] for idx in import_data['members'])
      self.wf_import_params['workflow member'] = import_members
    if import_data['admins']:
      import_owners = '\n'.join(
          self.user_emails[idx] for idx in import_data['admins'])
      self.wf_import_params['admin'] = import_owners
    resp = self.import_data(self.wf_import_params)
    if is_success:
      self.assertEqual(resp[0][success_resp_action], 1)
      self._check_csv_response(resp, {})
      workflow = Workflow.eager_query().filter(
          Workflow.slug == self.wf_slug).first()

      exst_admins = [acl.person.email for acl in workflow.access_control_list
                     if acl.ac_role.name == 'Admin']
      expected_admins = [self.user_emails[idx]
                         for idx in expected_data['admins']]
      self.assertItemsEqual(exst_admins, expected_admins)

      exst_members = [acl.person.email for acl in workflow.access_control_list
                      if acl.ac_role.name == 'Workflow Member']
      expected_members = [self.user_emails[idx]
                          for idx in expected_data['members']]
      self.assertItemsEqual(exst_members, expected_members)
    else:
      self.assertEqual(resp[0]['ignored'], 1)

  @ddt.data(
      {
          'import_data': {
              'admins': [0, 1],
              'members': [2, 3]
          },
          'expected_data': {
              'admins': [0, 1],
              'members': [2, 3]
          }
      },
      {
          'import_data': {
              'admins': [0, 1],
              'members': [1, 2]
          },
          'expected_data': {
              'admins': [0, 1],
              'members': [1, 2]
          }
      },
      {
          'import_data': {
              'admins': [0, 1],
              'members': [0, 1]
          },
          'expected_data': {
              'admins': [0, 1],
              'members': [0, 1]
          }
      },
      {
          'import_data': {
              'admins': [0, 1],
              'members': []
          },
          'expected_data': {
              'admins': [0, 1],
              'members': []
          }
      },
      {
          'import_data': {
              'admins': [],
              'members': [0, 1]
          },
          'is_success': False
      },
      {
          'import_data': {
              'admins': [],
              'members': []
          },
          'is_success': False
      }
  )
  @ddt.unpack
  def test_create_workflow_with_people(self, import_data, expected_data=None,
                                       is_success=True):
    """Tests importing new workflow with data: {import_data}."""
    self._check_workflow_people(import_data, expected_data, is_success,
                                'created')

  @ddt.data(
      {
          'import_data': {
              'admins': [0, 1],
              'members': [2, 3]
          },
          'expected_data': {
              'admins': [0, 1],
              'members': [2, 3]
          }
      },
      {
          'import_data': {
              'admins': [0, 1],
              'members': [1, 2]
          },
          'expected_data': {
              'admins': [0, 1],
              'members': [1, 2]
          }
      },
      {
          'import_data': {
              'admins': [0, 1],
              'members': [0, 1]
          },
          'expected_data': {
              'admins': [0, 1],
              'members': [0, 1]
          }
      },
      {
          'import_data': {
              'admins': [0, 1],
              'members': []
          },
          'expected_data': {
              'admins': [0, 1],
              'members': [6, 7]
          }
      },
      {
          'import_data': {
              'admins': [6, 7],
              'members': []
          },
          'expected_data': {
              'admins': [6, 7],
              'members': [6, 7]
          }
      },
      {
          'import_data': {
              'admins': [],
              'members': [0, 1]
          },
          'expected_data': {
              'admins': [4, 5],
              'members': [0, 1]
          }
      },
      {
          'import_data': {
              'admins': [],
              'members': []
          },
          'expected_data': {
              'admins': [4, 5],
              'members': [6, 7]
          }
      },
      {
          'import_data': {
              'admins': [],
              'members': [4, 5]
          },
          'expected_data': {
              'admins': [4, 5],
              'members': [4, 5]
          }
      }
  )
  @ddt.unpack
  def test_update_workflow_with_people(self, import_data, expected_data):
    """Tests importing existing workflow with data: {import_data}."""
    self.wf_import_params['admin'] = '\n'.join((self.user_emails[4],
                                                self.user_emails[5]))
    self.wf_import_params['workflow member'] = '\n'.join((self.user_emails[6],
                                                          self.user_emails[7]))
    self.import_data(self.wf_import_params)
    self._check_workflow_people(import_data, expected_data, True, 'updated')
