# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Mapping rules for Relationship validation and map:model import columns."""

def get_mapping_rules():
  """ Get mappings rules as defined in business_object.js

  Special cases:
    Aduit has direct mapping to Program with program_id
    Section has a direct mapping to Standard/Regulation/Poicy with directive_id
  """
  # these rules are copy pasted from
  # src/ggrc/assets/javascripts/apps/base_widgets.js line: 9
  # WARNING ########################################################
  # Manually added Risks and threats to the list from base_widgets #
  ##################################################################
  # TODO: Read these rules from different modules and combine them here.
  all_rules = set(['AccessGroup', 'Assessment', 'Audit', 'Clause', 'Contract',
                   'Control', 'CycleTaskGroupObjectTask', 'DataAsset',
                   'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
                   'Person', 'Policy', 'Process', 'Product', 'Program',
                   'Project', 'Regulation', 'Risk', 'Section', 'Standard',
                   'System', 'Threat', 'Vendor'])

  business_object_rules = {
      "AccessGroup": all_rules - set(['AccessGroup']),
      "Assessment": all_rules - set(['Assessment']),
      "Audit": all_rules - set(['CycleTaskGroupObjectTask', 'Audit',
                                'Risk', 'Threat']),
      "Clause": all_rules - set(['Clause']),
      "Contract": all_rules - set(['Policy', 'Regulation',
                                   'Contract', 'Standard']),
      "Control": all_rules,
      "CycleTaskGroupObjectTask": all_rules - set(['CycleTaskGroupObjectTask',
                                                   'Audit']),
      "DataAsset": all_rules,
      "Facility": all_rules,
      "Issue": all_rules,
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
      "Risk": all_rules - set(['Audit', 'Risk']),
      "Section": all_rules,
      "Standard": all_rules - set(['Policy', 'Regulation',
                                   'Contract', 'Standard']),
      "System": all_rules,
      "Threat": all_rules - set(['Audit', 'Threat']),
      "Vendor": all_rules,
  }

  return business_object_rules


def get_unmapping_rules():
  """Get unmapping rules from mapping dict."""
  return get_mapping_rules()


__all__ = [
    "get_mapping_rules",
    "get_unmapping_rules",
]
