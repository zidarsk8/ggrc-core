/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/tree-item-custom-attribute.mustache';

(function (can, GGRC) {
  'use strict';

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
