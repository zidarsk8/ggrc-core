# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Automapping rules generator."""

import itertools
from logging import getLogger


class AutomappingRuleConfigError(ValueError):
  pass


TYPE_ORDERING = [['Program'],
                 ['Regulation', 'Policy', 'Standard', 'Contract'],
                 ['Section', 'Clause'], ['Objective'], ['Control']]

# pylint: disable=invalid-name
logger = getLogger(__name__)


def get_type_indices():
  """Translate TYPE_ORDERING into type->level map to check rule ordering."""
  indices = dict()
  for i, layer in enumerate(TYPE_ORDERING):
    for type_ in layer:
      indices[type_] = i
  return indices


Rule = collections.namedtuple("Rule", ["name", "top", "mid", "bottom"])


class RuleSet(object):
  """Automapping Rule collection with validation logic."""
  entry_empty = frozenset()
  _type_indices = get_type_indices()

  @classmethod
  def _assert_type_order(cls, higher, lower):
    """Raise exception if types higher and lower violate type ordering."""
    i1 = cls._type_indices.get(higher)
    if i1 is None:
      raise AutomappingRuleConfigError("Unknown level for {}".format(higher))
    i2 = cls._type_indices.get(lower)
    if i2 is None:
      raise AutomappingRuleConfigError("Unknown level for {}".format(higher))
    if not i1 <= i2:
      raise AutomappingRuleConfigError("Type {} must be higher than type {}"
                                       .format(higher, lower))

  @classmethod
  def _explode_rules(cls, rule_list):
    for rule in rule_list:
      for top, mid, bottom in itertools.product(rule.top, rule.mid,
                                                rule.bottom):
        cls._assert_type_order(higher=top, lower=mid)
        cls._assert_type_order(higher=mid, lower=bottom)
        yield (bottom, mid, top, rule)
        yield (top, mid, bottom, rule)

  def __init__(self, count_limit, rule_list):
    self.count_limit = count_limit
    self._rule_list = rule_list
    self._rules = dict()
    self._rule_source = dict()

    # TODO: rewrite so that "for src, dst, mapping, source in ..." works
    for dst, src, mapping, source in self._explode_rules(rule_list):
      key = (src, dst)
      entry = self._rules.get(key, self.entry_empty)
      entry = entry | {mapping}
      self._rules[key] = entry

      sources = self._rule_source.get((src, dst, mapping), set())
      sources.add(source)
      self._rule_source[src, dst, mapping] = sources

    self._freeze()

  def _freeze(self):
    for key in self._rules:
      entry = self._rules[key]
      self._rules[key] = frozenset(entry)

  def __getitem__(self, key):
    return self._rules.get(key, RuleSet.entry_empty)

  def __repr__(self):
    return 'Rules(%s)' % repr(self._rule_list)

  def __str__(self):
    lines = []
    for key in self._rules:
      src, dst = key
      for mapping in self._rules[key]:
        source = ','.join(r.name for r in self._rule_source[src, dst, mapping])
        rule = ('  -> %s <--> %s <--> %s <- )' % (dst, src, mapping))
        rule += ' ' * (70 - len(rule))
        rule += source
        lines.append(rule)
    lines.sort()
    return 'RulesSet\n' + '\n'.join(lines)


class Types(object):
  """Model names and collections to use in Rule initialization."""
  all = {'Program', 'Regulation', 'Policy', 'Standard', 'Contract',
         'Section', 'Clause', 'Objective', 'Control'}
  directives = {'Regulation', 'Policy', 'Standard', 'Contract'}
  assets_business = {'System', 'Process', 'DataAsset', 'Product', 'Project',
                     'Facility', 'Market'}
  people_groups = {'AccessGroup', 'Person', 'OrgGroup', 'Vendor'}


rules = RuleSet(count_limit=10000, rule_list=[
    Rule(
        'mapping directive to a program',
        {'Program'},
        Types.directives,
        Types.all - {'Program'} - Types.directives,
    ),

    Rule(
        'mapping to sections and clauses',
        Types.directives,
        {'Section', 'Clause'},
        {'Objective', 'Control'},
    ),

    Rule(
        'mapping to objective',
        {'Section'},
        {'Objective'},
        {'Objective', 'Control'},
    ),

    Rule(
        'mapping nested controls',
        {'Objective'},
        {'Control'},
        {'Control'},
    ),

])
