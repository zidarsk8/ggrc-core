# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

from collections import namedtuple
from ggrc import models

Rule = namedtuple('Rule', ['src', 'mappings', 'dst'])
Attr = namedtuple('Attr', ['name'])


class RuleSet(object):
  Entry = namedtuple('RuleSetEntry', ['explicit', 'implicit'])
  entry_empty = Entry(frozenset(set()), frozenset(set()))

  def __init__(self, rule_list):
    rules = dict()

    def relate(src, dst):
      if src < dst:
        return (src, dst)
      else:
        return (dst, src)

    def wrap(o):
      if isinstance(o, set):
        return o
      else:
        return {o}

    def available(m, l):
      return hasattr(getattr(models, m), l + '_id')

    for rule in rule_list:
      for src in wrap(rule.src):
        for dst in wrap(rule.dst):
          key = (src, dst)
          existing_rules = (rules[key]
                            if key in rules else RuleSet.Entry(set(), set()))
          mappings = wrap(rule.mappings)
          explicit = set(obj for obj in mappings
                         if isinstance(obj, str))
          implicit = set(obj for obj in mappings
                         if isinstance(obj, Attr) and available(src, obj.name))

          rules[key] = RuleSet.Entry(existing_rules.explicit | explicit,
                                     existing_rules.implicit | implicit)
    for key in rules:
      explicit, implicit = rules[key]
      rules[key] = RuleSet.Entry(frozenset(explicit), frozenset(implicit))
    self._rule_list = rule_list
    self._rules = rules

  def __getitem__(self, key):
    if key in self._rules:
      return self._rules[key]
    else:
      return RuleSet.entry_empty

  def __repr__(self):
    return 'Rules(%s)' % repr(self._rule_list)

  def __str__(self):
    rules = []
    for key in self._rules:
      src, dst = key
      for mapping in self._rules[key].explicit | self._rules[key].implicit:
        rules.append('  -> %s <--> %s <--> %s <-' % (dst, src, mapping))
    rules.sort()
    return 'RulesSet\n' + '\n'.join(rules)


class Types(object):
  all = {'Audit', 'Clause', 'Contract', 'Control', 'ControlAssessment',
         'Issue', 'Objective', 'Policy', 'Program', 'Project', 'Regulation',
         'Request', 'Section', 'Standard'}
  directives = {'Regulation', 'Policy', 'Standard', 'Contract', 'Clause',
                'Section'}
  objectives = {'Control', 'Objective'}
  assets_business = {'System', 'Process', 'DataAsset', 'Product', 'Project',
                     'Facility', 'Market'}
  people_groups = {'Person', 'OrgGroup', 'Vendor'}


mapping_to_a_program = Rule(
    'Program',
    Types.directives,
    (Types.all - {'Audit'} - Types.directives |
     Types.assets_business | Types.people_groups),
)

mapping_directive_to_a_program = Rule(
    Types.directives,
    Types.all - {'Program'},
    'Program',
)

mapping_to_sections_and_clauses = Rule(
    {'Section', 'Clause'},
    Attr('directive'),
    Types.all,
)

mapping_to_objective = Rule(
    Types.objectives,
    {'Section'},
    Types.all,
)

rules = RuleSet([
    mapping_to_a_program,
    mapping_directive_to_a_program,
    mapping_to_sections_and_clauses,
    mapping_to_objective,
])
