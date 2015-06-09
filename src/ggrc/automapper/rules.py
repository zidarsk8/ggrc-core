# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

from collections import namedtuple

Rule = namedtuple('Rule', ['src', 'mappings', 'dst'])

class RuleSet(object):
  def __init__(self, rule_list):
    rules = dict()
    for rule in rule_list:
      wrap = lambda o: o if isinstance(o, set) else {o}
      for src in wrap(rule.src):
        for dst in wrap(rule.dst):
          if src > dst:
            src, dst = dst, src
          rules[(src,dst)] = frozenset(wrap(rule.mappings))
    self._rule_list = rule_list
    self._rules = rules

  def  __getitem__(self, key): 
    (src, dst) = key
    if src > dst:
      src, dst = dst, src
    key = (src, dst)
    if key in self._rules:
      return self._rules[key]
    else:
      return None

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

rules= RuleSet([
    mapping_directive_to_a_program,
    mapping_directive_to_a_program,
    mapping_to_sections_and_clauses,
    mapping_to_objective,
])
