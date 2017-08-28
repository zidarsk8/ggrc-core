# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit tests for rules generator."""

from unittest import TestCase

import mock

from ggrc.automapper import rules


class TestRuleSet(TestCase):
  """Unit tests for rule set container."""

  MOCK_TYPE_ORDERING = [["TopLevel"],
                        ["UpperMidLevel1", "UpperMidLevel2"],
                        ["LowerMidLevel1", "LowerMidLevel2"],
                        ["BottomLevel1", "BottomLevel2", "BottomLevel3"]]

  @mock.patch("ggrc.automapper.rules.TYPE_ORDERING", new=MOCK_TYPE_ORDERING)
  def test_explode_rules_ok(self):
    rule1 = rules.Rule("T - UM1,LM1 - B1, B3",
                       {"TopLevel"},
                       {"UpperMidLevel1", "LowerMidLevel1"},
                       {"BottomLevel1", "BottomLevel3"})
    rule2 = rules.Rule("T - T - B2",
                       {"TopLevel"},
                       {"TopLevel"},
                       {"BottomLevel2"})
    rule3 = rules.Rule("UM2 - LM1 - LM1",
                       {"UpperMidLevel2"},
                       {"LowerMidLevel1"},
                       {"LowerMidLevel1"})
    rule_list = [rule1, rule2, rule3]

    rules.RuleSet._type_indices = rules.get_type_indices()

    result = rules.RuleSet._explode_rules(rule_list)

    self.assertEqual(
        sorted(result),
        sorted([
            # rule1 - straight
            ("TopLevel", "UpperMidLevel1", "BottomLevel1", rule1),
            ("TopLevel", "UpperMidLevel1", "BottomLevel3", rule1),
            ("TopLevel", "LowerMidLevel1", "BottomLevel1", rule1),
            ("TopLevel", "LowerMidLevel1", "BottomLevel3", rule1),
            # rule1 - reverse
            ("BottomLevel1", "LowerMidLevel1", "TopLevel", rule1),
            ("BottomLevel3", "LowerMidLevel1", "TopLevel", rule1),
            ("BottomLevel1", "UpperMidLevel1", "TopLevel", rule1),
            ("BottomLevel3", "UpperMidLevel1", "TopLevel", rule1),
            # rule2 - straight
            ("TopLevel", "TopLevel", "BottomLevel2", rule2),
            # rule2 - reverse
            ("BottomLevel2", "TopLevel", "TopLevel", rule2),
            # rule3 - straight
            ("UpperMidLevel2", "LowerMidLevel1", "LowerMidLevel1", rule3),
            # rule3 - reverse
            ("LowerMidLevel1", "LowerMidLevel1", "UpperMidLevel2", rule3),
        ]),
    )

  @mock.patch("ggrc.automapper.rules.TYPE_ORDERING", new=MOCK_TYPE_ORDERING)
  def test_explode_rules_wrong_order(self):
    rule = rules.Rule("TopLevel is after LowerMidLevel1",
                      {"LowerMidLevel1"},
                      {"TopLevel"},
                      {"BottomLevel1"})

    rules.RuleSet._type_indices = rules.get_type_indices()

    with self.assertRaises(rules.AutomappingRuleConfigError):
      for _ in rules.RuleSet._explode_rules([rule]):
        # force the generator to yield all values
        pass

  @mock.patch("ggrc.automapper.rules.TYPE_ORDERING", new=MOCK_TYPE_ORDERING)
  def test_explode_rules_unknown_type(self):
    rule = rules.Rule("Lists unknown type",
                      {"TopLevel"},
                      {"UnknownType"},
                      {"BottomLevel1"})

    rules.RuleSet._type_indices = rules.get_type_indices()

    with self.assertRaises(rules.AutomappingRuleConfigError):
      for _ in rules.RuleSet._explode_rules([rule]):
        # force the generator to yield all values
        pass
