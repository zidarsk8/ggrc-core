/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/tree-no-results.mustache';

(function (can, GGRC) {
  'use strict';

  GGRC.Components('treeNoResults', {
    tag: 'tree-no-results',
    template: template,
    viewModel: {
      define: {
        text: {
          value: 'No results, please check your filter criteria',
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
