/*
  Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import BaseTreePeopleVM from '../view-models/tree-people-base-vm';

const viewModel = BaseTreePeopleVM.extend({
  role: null,
  getSourceList: function () {
    let roleName = this.attr('role');
    let instance = this.attr('source');
    return GGRC.Utils.peopleWithRoleName(instance, roleName);
  },
});

export default GGRC.Components('treePeopleWithRoleListField', {
  tag: 'tree-people-with-role-list-field',
  template: '{{peopleStr}}',
  viewModel: viewModel,
  events: {
    '{viewModel.source} change': function () {
      this.viewModel.refreshPeople();
    },
  },
});
