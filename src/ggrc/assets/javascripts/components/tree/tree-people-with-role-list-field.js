/*!
  Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, GGRC) {
  'use strict';

  var viewModel = GGRC.VM.BaseTreePeopleField.extend({
    role: null,
    getSourceList: function () {
      var roleName = this.attr('role');
      var instance = this.attr('source');
      return GGRC.Utils.peopleWithRoleName(instance, roleName);
    }
  });

  GGRC.Components('treePeopleWithRoleListField', {
    tag: 'tree-people-with-role-list-field',
    template: '{{peopleStr}}',
    viewModel: viewModel,
    events: {
      '{viewModel.source} change': function () {
        this.viewModel.refreshPeople();
      }
    }
  });
})(window.can, window.GGRC);
