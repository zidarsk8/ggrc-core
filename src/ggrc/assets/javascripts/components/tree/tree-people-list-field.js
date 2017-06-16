/*!
  Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, GGRC) {
  'use strict';

  var viewModel = GGRC.VM.BaseTreePeopleField.extend({
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

  GGRC.Components('treePeopleListField', {
    tag: 'tree-people-list-field',
    template: '<content />',
    viewModel: viewModel,
    events: {
      '{viewModel} source': function () {
        this.viewModel.refreshPeople();
      },
      '{viewModel.source} change': function () {
        this.viewModel.refreshPeople();
      }
    }
  });
})(window.can, window.GGRC);
