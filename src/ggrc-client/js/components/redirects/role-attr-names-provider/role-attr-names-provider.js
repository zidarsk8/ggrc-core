/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanComponent from 'can-component';
const roleToLinkMap = {
  Control: {
    Admin: 'owner',
    'Control Operators': 'control_operator',
    'Control Owners': 'control_owner',
    'Principal Assignees': 'principal_assignee',
    'Secondary Assignees': 'secondary_assignee',
    'Other Contacts': 'other_contact',
  },
  Risk: {
    Admin: 'owner',
    'Risk Owners': 'risk_owner',
    'Other Contacts': 'other_contact',
  },
};

const viewModel = can.Map.extend({
  define: {
    linkAttrName: {
      get() {
        return roleToLinkMap[this.attr('modelType')][this.attr('roleName')];
      },
    },
  },
  modelType: '',
  roleName: '',
});

export default CanComponent.extend({
  tag: 'role-attr-names-provider',
  viewModel,
});
