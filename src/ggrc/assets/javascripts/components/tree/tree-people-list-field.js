/*
  Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import BaseTreePeopleVM from '../view-models/tree-people-base-vm';
import template from './templates/tree-people-list-field.mustache';

const viewModel = BaseTreePeopleVM.extend({
  filter: '@',
  getSourceList: function () {
    let filter = this.attr('filter');
    let sourceString = 'source';

    if (filter) {
      sourceString += '.' + filter;
    }

    return can.makeArray(this.attr(sourceString));
  },
});

GGRC.Components('treePeopleListField', {
  tag: 'tree-people-list-field',
  template: template,
  viewModel: viewModel,
  events: {
    '{viewModel} source': function () {
      this.viewModel.refreshPeople();
    },
  },
});
