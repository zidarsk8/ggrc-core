# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Automapping rules generator."""

import collections
import itertools
from logging import getLogger


class AutomappingRuleConfigError(ValueError):
  pass


TYPE_ORDERING = [['Program'],
                 ['Regulation', 'Policy', 'Standard', 'Contract'],
                 ['Section', 'Clause'], ['Objective'], ['Control']]

# pylint: disable=invalid-name
logger = getLogger(__name__)


def get_type_levels():
  """Translate TYPE_ORDERING into type->level map to check rule ordering."""
  indices = dict()
  for i, layer in enumerate(TYPE_ORDERING):
    for type_ in layer:
      indices[type_] = i
  return indices


Rule = collections.namedtuple("Rule", ["top", "mid", "bottom"])


class RuleSet(collections.defaultdict):
  """Automapping Rule collection with validation logic."""
  DEFAULT = frozenset()
  _type_levels = get_type_levels()

  @classmethod
  def _assert_type_order(cls, *type_sets):
    """Raise exception if types violate type ordering.

    In a correct Rule, the levels of types must not be decreasing.
    """
    try:
      levels = [{(cls._type_levels[type_])
                 for type_ in set_}
                for set_ in type_sets]
    except KeyError as e:
      raise AutomappingRuleConfigError("Unknown level for {}"
                                       .format(e.args[0]))

    for i, level in enumerate(levels[1:], 1):
      if max(level) < min(levels[i - 1]):
        raise AutomappingRuleConfigError(
            "All types {} must be higher than all types {}"
            .format(type_sets[i - 1], type_sets[i]))

  @classmethod
  def _explode_rules(cls, rule_list):
    for rule in rule_list:
      cls._assert_type_order(rule.top, rule.mid, rule.bottom)
      for top, mid, bottom in itertools.product(rule.top, rule.mid,
                                                rule.bottom):
        yield (bottom, mid, top)
        yield (top, mid, bottom)

  def __init__(self, rule_list):
    super(RuleSet, self).__init__(lambda: self.DEFAULT)

    # TODO: rewrite so that "for src, dst, mapping in ..." works
    for dst, src, mapping in self._explode_rules(rule_list):
      self[src, dst] |= {mapping}


class Types(object):
  """Model names and collections to use in Rule initialization."""
  all = {'Program', 'Regulation', 'Policy', 'Standard', 'Contract',
         'Section', 'Clause', 'Objective', 'Control'}
  directives = {'Regulation', 'Policy', 'Standard', 'Contract'}
  assets_business = {'System', 'Process', 'DataAsset', 'Product', 'Project',
                     'Facility', 'Market'}
  people_groups = {'AccessGroup', 'Person', 'OrgGroup', 'Vendor'}


rules = RuleSet(rule_list=[
    Rule(
        # mapping directive to a program
        {'Program'},
        Types.directives,
        Types.all - {'Program'} - Types.directives,
    ),

    Rule(
        # mapping to sections and clauses
        Types.directives,
        {'Section', 'Clause'},
        {'Objective', 'Control'},
    ),

    Rule(
        # mapping to objective
        {'Section'},
        {'Objective'},
        {'Objective', 'Control'},
    ),

    Rule(
        # mapping nested controls
        {'Objective'},
        {'Control'},
        {'Control'},
    ),

])
