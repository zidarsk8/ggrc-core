/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can, $) {
  'use strict';

  GGRC.Components('documentObjectList', {
    tag: 'document-object-list',
    template: can.view(
      GGRC.mustache_path +
      '/components/object-list/document-object-list.mustache'
    ),
    viewModel: {
      define: {
        noItemsText: {
          type: 'string',
          value: ''
        }
      },
      title: '@',
      tooltip: '@',
      limit: 5,
      instance: null,
      documents: [],
      header: '@'
    }
  });
})(window.GGRC, window.can, window.can.$);
