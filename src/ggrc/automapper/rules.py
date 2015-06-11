# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

from collections import namedtuple
from ggrc.utils import get_mapping_rules
import ipdb

Rule = namedtuple('Rule', ['src', 'mappings', 'dst'])

class RuleSet(object):
  def __init__(self, rule_list):
    rules = dict()
    allowed= get_mapping_rules()
    wrap = lambda o: o if isinstance(o, set) else {o}
    for rule in rule_list:
      for src in wrap(rule.src):
        for dst in wrap(rule.dst):
          key = (src, dst)
          existing_rules = rules[key] if key in rules else set()
          allowed_mappings = allowed[dst] if dst in allowed else set() 
          rules[key] = existing_rules | set(filter(allowed_mappings.__contains__, 
                                                   wrap(rule.mappings)))
    for key in rules:
      rules[key] = frozenset(rules[key])
    self._rule_list = rule_list
    self._rules = rules

  def  __getitem__(self, key): 
    if key in self._rules:
      return self._rules[key]
    else:
      return set()

  def __repr__(self):
    return 'Rules(%s)' % repr(self._rule_list)


class Types(object):
  all = {'Audit', 'Clause', 'Contract', 'Control', 'ControlAssessment', 
         'DataAsset', 'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup', 
         'Person', 'Policy', 'Process', 'Product', 'Program', 'Project', 
         'Regulation', 'Request', 'Section', 'Standard', 'System', 'Vendor'}
  directives = {'Regulation', 'Policy', 'Standard', 'Contract', 'Clause', 
                'Section'}
  objectives = {'Control', 'Objective'}


mapping_to_a_program = Rule(
    'Program', 
    Types.all - {'Audit'} - Types.directives,
    Types.directives,
)

mapping_directive_to_a_program = Rule(
    Types.directives,
    Types.all - {'Program'},
    'Program',
)

mapping_to_sections_and_clauses = Rule(
    {'Section', 'Clause'},
    Types.directives,
    Types.all,
)

mapping_to_objective = Rule(
    Types.objectives,
    Types.all,
    {'Section'},
)

test_mapping_issues = Rule(
    'Issue',
    'Issue',
    'Issue',
)

rules = RuleSet([
    mapping_directive_to_a_program,
    mapping_directive_to_a_program,
    mapping_to_sections_and_clauses,
    mapping_to_objective,
    # test_mapping_issues,
])
