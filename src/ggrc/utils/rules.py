# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Mapping rules for Relationship validation and map:model import columns."""

import copy


def get_mapping_rules():
  """ Get mappings rules as defined in business_object.js

  Special cases:
    Aduit has direct mapping to Program with program_id
    Section has a direct mapping to Standard/Regulation/Poicy with directive_id
  """
  from ggrc import snapshotter
  all_rules = set(['AccessGroup', 'Clause', 'Contract', 'Control',
                   'CycleTaskGroupObjectTask', 'DataAsset', 'Facility',
                   'Market', 'Objective', 'OrgGroup', 'Person', 'Policy',
                   'Process', 'Product', 'Program', 'Project', 'Regulation',
                   'Risk', 'Section', 'Standard', 'System', 'Threat',
                   'Vendor'])

  snapshots = snapshotter.rules.Types.all

  business_object_rules = {
      "AccessGroup": all_rules - set(['AccessGroup']),
      "Clause": all_rules - set(['Clause']),
      "Contract": all_rules - set(['Policy', 'Regulation',
                                   'Contract', 'Standard']),
      "Control": all_rules,
      "CycleTaskGroupObjectTask": (all_rules -
                                   set(['CycleTaskGroupObjectTask'])),
      "DataAsset": all_rules,
      "Facility": all_rules,
      "Market": all_rules,
      "Objective": all_rules,
      "OrgGroup": all_rules,
      "Person": all_rules - set(['Person']),
      "Policy": all_rules - set(['Policy', 'Regulation',
                                 'Contract', 'Standard']),
      "Process": all_rules,
      "Product": all_rules,
      "Program": all_rules - set(['Program']),
      "Project": all_rules,
      "Regulation": all_rules - set(['Policy', 'Regulation',
                                     'Contract', 'Standard']),
      "Risk": all_rules - set(['Risk']),
      "Section": all_rules,
      "Standard": all_rules - set(['Policy', 'Regulation',
                                   'Contract', 'Standard']),
      "System": all_rules,
      "Threat": all_rules - set(['Threat']),
      "Vendor": all_rules,
  }

  # Audit and Audit-scope objects
  # Assessment and Issue have a special Audit field instead of map:audit
  business_object_rules.update({
      "Audit": set(),
      "Assessment": snapshots | {"Issue"},
      "Issue": snapshots | {"Assessment"},
  })

  return business_object_rules


def get_unmapping_rules():
  """Get unmapping rules from mapping dict."""
  unmapping_rules = copy.deepcopy(get_mapping_rules())

  # Audit and Audit-scope objects
  unmapping_rules["Audit"] = set()
  unmapping_rules["Assessment"] = {"Issue"}
  unmapping_rules["Issue"] = {"Assessment"}

  return unmapping_rules


__all__ = [
    "get_mapping_rules",
    "get_unmapping_rules",
]
