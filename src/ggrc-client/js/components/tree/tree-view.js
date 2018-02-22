/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../sort/sort-by';
import template from './templates/tree-view.mustache';

(function (can, GGRC) {
  'use strict';

  let viewModel = can.Map.extend({
    define: {
      notResult: {
        type: Boolean,
        get: function () {
          return !this.attr('loading') && !this.attr('items').length;
        },
      },
    },
    items: [],
    parentInstance: null,
    model: null,
    selectedColumns: [],
    mandatory: [],
    disableConfiguration: null,
    loading: false,
    limitDepthTree: 0,
    depthFilter: '',
  });

  GGRC.Components('treeView', {
    tag: 'tree-view',
    template: template,
    viewModel: viewModel,
  });
})(window.can, window.GGRC);
