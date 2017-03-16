/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/tree/tree-no-results.mustache');

  GGRC.Components('treeNoResults', {
    tag: 'tree-no-results',
    template: template,
    viewModel: {
      define: {
        text: {
          set: function (value) {
            return value || 'No results...';
          }
        },
        show: {
          set: function (value) {
            return value || false;
          }
        }
      }
    }
  });
})(window.can, window.GGRC);
