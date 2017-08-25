# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Automapping rules generator."""

import itertools
from collections import namedtuple
from logging import getLogger


Attr = namedtuple('Attr', ['name'])


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
  Entry = namedtuple('RuleSetEntry', ['explicit', 'implicit'])
  entry_empty = Entry(frozenset(set()), frozenset(set()))
  _type_indices = get_type_indices()

  @classmethod
  def _check_type_order(cls, type1, type2):
    """Get error message if type1 and type2 violate type ordering."""
    i1 = cls._type_indices.get(type1, None)
    if i1 is None:
      return "Unknown level for %s" % type1
    i2 = cls._type_indices.get(type2, None)
    if i2 is None:
      return "Unknown level for %s" % type2
    if not i1 <= i2:
      return "Type %s does not occur higher than type %s" % (type1, type2)

  @classmethod
  def _explode_rules(cls, rule_list):
    for rule in rule_list:
      for top, mid, bottom in itertools.product(rule.top, rule.mid,
                                                rule.bottom):
        if Attr in map(type, [top, mid, bottom]):
          # if this is a direct mapping
          # there is only one way to form the triangle
          # TODO rule sanity check
          yield (mid, bottom, top, rule)
        else:
          err1 = cls._check_type_order(top, mid)
          err2 = cls._check_type_order(mid, bottom)
          if err1 is not None or err2 is not None:
            logger.warning("Automapping rule ordering violation")
            if err1 is not None:
              logger.warning(err1)
            if err2 is not None:
              logger.warning(err2)
            logger.warning("Skipping bad rule (%s, %s, %s)", top, mid, bottom)
            continue
          yield (mid, bottom, top, rule)
          yield (mid, top, bottom, rule)

  def __init__(self, count_limit, rule_list):
    self.count_limit = count_limit
    self._rule_list = rule_list
    self._rules = dict()
    self._rule_source = dict()

    for src, dst, mapping, source in self._explode_rules(rule_list):
      key = (src, dst)
      entry = self._rules.get(key, RuleSet.Entry(set(), set()))
      if isinstance(mapping, Attr):
        entry = RuleSet.Entry(entry.explicit, entry.implicit | {mapping})
      else:
        entry = RuleSet.Entry(entry.explicit | {mapping}, entry.implicit)
      self._rules[key] = entry

      sources = self._rule_source.get((src, dst, mapping), set())
      sources.add(source)
      self._rule_source[src, dst, mapping] = sources

    self._freeze()

  def _freeze(self):
    for key in self._rules:
      explicit, implicit = self._rules[key]
      self._rules[key] = RuleSet.Entry(frozenset(explicit),
                                       frozenset(implicit))

  def __getitem__(self, key):
    return self._rules.get(key, RuleSet.entry_empty)

  def __repr__(self):
    return 'Rules(%s)' % repr(self._rule_list)

  def __str__(self):
    lines = []
    for key in self._rules:
      src, dst = key
      for mapping in self._rules[key].explicit | self._rules[key].implicit:
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
