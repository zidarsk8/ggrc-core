/*!
  Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import BaseTreePeopleVM from '../view-models/tree-people-base-vm';

var viewModel = BaseTreePeopleVM.extend({
  filter: '@',
  getSourceList: function () {
    var filter = this.attr('filter');
    var sourceString = 'source';

    if (filter) {
      sourceString += '.' + filter;
    }

    return can.makeArray(this.attr(sourceString));
  }
});

export default GGRC.Components('treePeopleListField', {
  tag: 'tree-people-list-field',
  template: '{{peopleStr}}',
  viewModel: viewModel,
  events: {
    '{viewModel.source} change': function () {
      this.viewModel.refreshPeople();
    }
  }
});
