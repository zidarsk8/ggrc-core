# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Unit test for checking fields in mapping and unmapping."""

import unittest

from ddt import data, ddt, unpack

from ggrc import utils


class BaseTestMappingRules(unittest.TestCase):
  """Base TestCase for mapping and unmapping check."""

  rules = {}

  def assertRules(self, model, *rules):  # pylint: disable=C0103
    """Assert to check rules for current model in mapping rules."""
    self.assertIn(model, self.rules)
    self.assertEqual(set(rules), self.rules[model])


@ddt
class TestMappingRules(BaseTestMappingRules):
  """Test case for mapping rules."""

  rules = utils.get_mapping_rules()

  all_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause', 'Contract',
               'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
               'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
               'Person', 'Policy', 'Process', 'Product', 'Program',
               'Project', 'Regulation', 'Risk', 'Section', 'Standard',
               'System', 'Threat', 'Vendor', ]
  assessment_rules = ['AccessGroup', 'Audit', 'Clause', 'Contract',
                      'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                      'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                      'Person', 'Policy', 'Process', 'Product', 'Program',
                      'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                      'System', 'Threat', 'Vendor', ]
  audit_rules = ['AccessGroup', 'Assessment', 'Clause', 'Contract', 'Control',
                 'DataAsset', 'Facility', 'Issue', 'Market', 'Objective',
                 'OrgGroup', 'Person', 'Policy', 'Process', 'Product',
                 'Program', 'Project', 'Regulation', 'Section', 'Standard',
                 'System', 'Vendor', ]
  accessgroup_rules = ['Assessment', 'Audit', 'Clause', 'Contract',
                       'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                       'Facility', 'Issue', 'Market', 'Objective',
                       'OrgGroup', 'Person', 'Policy', 'Process', 'Product',
                       'Program', 'Project', 'Regulation', 'Risk',
                       'Section', 'Standard', 'System', 'Threat', 'Vendor', ]
  contract_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause',
                    'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                    'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                    'Person', 'Process', 'Product', 'Program', 'Project',
                    'Risk', 'Section', 'System', 'Threat', 'Vendor', ]
  cycletaskgroupobjecttask_rules = ['AccessGroup', 'Assessment',
                                    'Clause', 'Contract', 'Control',
                                    'DataAsset', 'Facility', 'Issue', 'Market',
                                    'Objective', 'OrgGroup', 'Person',
                                    'Policy', 'Process', 'Product', 'Program',
                                    'Project', 'Regulation', 'Risk',
                                    'Section', 'Standard', 'System',
                                    'Threat', 'Vendor', ]
  clause_rules = ['AccessGroup', 'Assessment', 'Audit', 'Contract',
                  'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                  'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                  'Person', 'Policy', 'Process', 'Product', 'Program',
                  'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                  'System', 'Threat', 'Vendor', ]
  person_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause', 'Contract',
                  'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                  'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                  'Policy', 'Process', 'Product', 'Program',
                  'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                  'System', 'Threat', 'Vendor', ]
  policy_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause',
                  'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                  'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                  'Person', 'Process', 'Product', 'Program',
                  'Project', 'Risk', 'Section', 'System', 'Threat', 'Vendor', ]
  program_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause', 'Contract',
                   'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                   'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                   'Person', 'Policy', 'Process', 'Product',
                   'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                   'System', 'Threat', 'Vendor', ]
  regulation_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause',
                      'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                      'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                      'Person', 'Process', 'Product', 'Program',
                      'Project', 'Risk', 'Section',
                      'System', 'Threat', 'Vendor', ]
  risk_rules = ['AccessGroup', 'Assessment', 'Clause', 'Contract',
                'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                'Person', 'Policy', 'Process', 'Product', 'Program',
                'Project', 'Regulation', 'Section', 'Standard',
                'System', 'Threat', 'Vendor', ]
  standard_rules = ['AccessGroup', 'Audit', 'Assessment', 'Clause',
                    'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                    'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                    'Person', 'Process', 'Product', 'Program', 'Project',
                    'Risk', 'Section', 'System', 'Threat', 'Vendor', ]
  threat_rules = ['AccessGroup', 'Assessment', 'Clause', 'Contract',
                  'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                  'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                  'Person', 'Policy', 'Process', 'Product', 'Program',
                  'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                  'System', 'Vendor', ]

  @data(("AccessGroup", accessgroup_rules),
        ("Assessment", assessment_rules),
        ("Audit", audit_rules),
        ("Clause", clause_rules),
        ("Contract", contract_rules),
        ("Control", all_rules),
        ("CycleTaskGroupObjectTask", cycletaskgroupobjecttask_rules),
        ("DataAsset", all_rules),
        ("Facility", all_rules),
        ("Issue", all_rules),
        ("Market", all_rules),
        ("Objective", all_rules),
        ("OrgGroup", all_rules),
        ("Person", person_rules),
        ("Policy", policy_rules),
        ("Process", all_rules),
        ("Product", all_rules),
        ("Program", program_rules),
        ("Project", all_rules),
        ("Regulation", regulation_rules),
        ("Risk", risk_rules),
        ("Section", all_rules),
        ("Standard", standard_rules),
        ("System", all_rules),
        ("Threat", threat_rules),
        ("Vendor", all_rules))
  @unpack
  def test_field(self, field, rules):
    self.assertRules(field, *rules)


@ddt
class TestUnMappingRules(BaseTestMappingRules):
  """Test case for unmapping rules."""

  rules = utils.get_unmapping_rules()

  all_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause', 'Contract',
               'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
               'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
               'Person', 'Policy', 'Process', 'Product', 'Program',
               'Project', 'Regulation', 'Risk', 'Section', 'Standard',
               'System', 'Threat', 'Vendor', ]
  assessment_rules = ['AccessGroup', 'Audit', 'Clause', 'Contract',
                      'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                      'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                      'Person', 'Policy', 'Process', 'Product', 'Program',
                      'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                      'System', 'Threat', 'Vendor', ]
  audit_rules = ['AccessGroup', 'Assessment', 'Clause', 'Contract', 'Control',
                 'DataAsset', 'Facility', 'Issue', 'Market', 'Objective',
                 'OrgGroup', 'Person', 'Policy', 'Process', 'Product',
                 'Program', 'Project', 'Regulation', 'Section', 'Standard',
                 'System', 'Vendor', ]
  accessgroup_rules = ['Assessment', 'Audit', 'Clause', 'Contract',
                       'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                       'Facility', 'Issue', 'Market', 'Objective',
                       'OrgGroup', 'Person', 'Policy', 'Process', 'Product',
                       'Program', 'Project', 'Regulation', 'Risk',
                       'Section', 'Standard', 'System', 'Threat', 'Vendor', ]
  contract_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause',
                    'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                    'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                    'Person', 'Process', 'Product', 'Program', 'Project',
                    'Risk', 'Section', 'System', 'Threat', 'Vendor', ]
  cycletaskgroupobjecttask_rules = ['AccessGroup', 'Assessment',
                                    'Clause', 'Contract', 'Control',
                                    'DataAsset', 'Facility', 'Issue', 'Market',
                                    'Objective', 'OrgGroup', 'Person',
                                    'Policy', 'Process', 'Product', 'Program',
                                    'Project', 'Regulation', 'Risk',
                                    'Section', 'Standard', 'System',
                                    'Threat', 'Vendor', ]
  clause_rules = ['AccessGroup', 'Assessment', 'Audit', 'Contract',
                  'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                  'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                  'Person', 'Policy', 'Process', 'Product', 'Program',
                  'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                  'System', 'Threat', 'Vendor', ]
  person_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause', 'Contract',
                  'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                  'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                  'Policy', 'Process', 'Product', 'Program',
                  'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                  'System', 'Threat', 'Vendor', ]
  policy_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause',
                  'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                  'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                  'Person', 'Process', 'Product', 'Program',
                  'Project', 'Risk', 'Section', 'System', 'Threat', 'Vendor', ]
  program_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause', 'Contract',
                   'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                   'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                   'Person', 'Policy', 'Process', 'Product',
                   'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                   'System', 'Threat', 'Vendor', ]
  regulation_rules = ['AccessGroup', 'Assessment', 'Audit', 'Clause',
                      'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                      'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                      'Person', 'Process', 'Product', 'Program',
                      'Project', 'Risk', 'Section',
                      'System', 'Threat', 'Vendor', ]
  risk_rules = ['AccessGroup', 'Assessment', 'Clause', 'Contract',
                'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                'Person', 'Policy', 'Process', 'Product', 'Program',
                'Project', 'Regulation', 'Section', 'Standard',
                'System', 'Threat', 'Vendor', ]
  standard_rules = ['AccessGroup', 'Audit', 'Assessment', 'Clause',
                    'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                    'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                    'Person', 'Process', 'Product', 'Program', 'Project',
                    'Risk', 'Section', 'System', 'Threat', 'Vendor', ]
  threat_rules = ['AccessGroup', 'Assessment', 'Clause', 'Contract',
                  'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                  'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                  'Person', 'Policy', 'Process', 'Product', 'Program',
                  'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                  'System', 'Vendor', ]

  @data(("AccessGroup", accessgroup_rules),
        ("Assessment", assessment_rules),
        ("Audit", audit_rules),
        ("Clause", clause_rules),
        ("Contract", contract_rules),
        ("Control", all_rules),
        ("CycleTaskGroupObjectTask", cycletaskgroupobjecttask_rules),
        ("DataAsset", all_rules),
        ("Facility", all_rules),
        ("Issue", all_rules),
        ("Market", all_rules),
        ("Objective", all_rules),
        ("OrgGroup", all_rules),
        ("Person", person_rules),
        ("Policy", policy_rules),
        ("Process", all_rules),
        ("Product", all_rules),
        ("Program", program_rules),
        ("Project", all_rules),
        ("Regulation", regulation_rules),
        ("Risk", risk_rules),
        ("Section", all_rules),
        ("Standard", standard_rules),
        ("System", all_rules),
        ("Threat", threat_rules),
        ("Vendor", all_rules))
  @unpack
  def test_field(self, field, rules):
    self.assertRules(field, *rules)
