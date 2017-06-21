/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, Mustache) {
  'use strict';

  GGRC.Components('deletablePeopleGroup', {
    tag: 'deletable-people-group',
    template: can.view(
      GGRC.mustache_path +
      '/components/people/deletable-people-group.mustache'
    ),
    viewModel: {
      define: {
        peopleLength: {
          get: function () {
            return this.attr('people').length;
          }
        },
        emptyListMessage: {
          type: 'string',
          value: ''
        }
      },
      required: '@',
      people: [],
      groupId: '@',
      canUnmap: true,
      instance: {},
      isLoading: false,
      withDetails: false,
      unmap: function (person) {
        this.dispatch({
          type: 'unmap',
          person: person,
          groupId: this.attr('groupId')
        });
      }
    }
  });
})(window.can, window.GGRC, can.Mustache);
