# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

from collections import namedtuple
import itertools
from ggrc import models

Attr = namedtuple('Attr', ['name'])


class Rule(object):
  def __init__(self, name, src, mappings, dst):
    def wrap(o):
      return o if isinstance(o, set) else {o}
    self.name = name
    self.src = wrap(src)
    self.mappings = wrap(mappings)
    self.dst = wrap(dst)


class RuleSet(object):
  Entry = namedtuple('RuleSetEntry', ['explicit', 'implicit'])
  entry_empty = Entry(frozenset(set()), frozenset(set()))

  def __init__(self, rule_list):
    self._rule_list = rule_list
    self._rules = dict()
    self._rule_source = dict()

    def available(m, l):
      return hasattr(getattr(models, m), l + '_id')

    for rule in rule_list:
      for src, dst in itertools.product(rule.src, rule.dst):
        key = (src, dst)
        existing_rules = self._rules.get(key, RuleSet.Entry(set(), set()))
        explicit = set(obj for obj in rule.mappings
                       if isinstance(obj, str))
        implicit = set(obj for obj in rule.mappings
                       if isinstance(obj, Attr) and available(src, obj.name))

        for obj in explicit | implicit:
          self._rule_source[src, dst, obj] = rule
        self._rules[key] = RuleSet.Entry(existing_rules.explicit | explicit,
                                         existing_rules.implicit | implicit)
    self._freeze()

  def _freeze(self):
    for key in self._rules:
      explicit, implicit = self._rules[key]
      self._rules[key] = RuleSet.Entry(frozenset(explicit),
                                       frozenset(implicit))

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
        source = self._rule_source[src, dst, mapping].name
        rule = ('  -> %s <--> %s <--> %s <- )' % (dst, src, mapping))
        rule += ' ' * (70 - len(rule))
        rule += source
        rules.append(rule)
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


rules = RuleSet([
    Rule(
        'mapping to a program',
        'Program',
        Types.directives,
        (Types.all - {'Audit'} - Types.directives |
         Types.assets_business | Types.people_groups),
    ),

    Rule(
        'mapping directive to a program',
        Types.directives,
        Types.all - {'Program'},
        'Program',
    ),

    Rule(
        'mapping to sections and clauses',
        {'Section', 'Clause'},
        Attr('directive'),
        Types.all,
    ),

    Rule(
        'mapping to objective',
        Types.objectives,
        {'Section'},
        Types.all,
    ),
])
