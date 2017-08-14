/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/tree/tree-item-custom-attribute.mustache');

  var viewModel = can.Map.extend({
    instance: null,
    values: [],
    column: {}
  });

  GGRC.Components('treeItemCustomAttribute', {
    tag: 'tree-item-custom-attribute',
    template: template,
    viewModel: viewModel
  });
})(window.can, window.GGRC);
