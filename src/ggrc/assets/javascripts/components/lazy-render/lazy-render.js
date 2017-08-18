/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var viewModel = can.Map.extend({
    define: {
      trigger: {
        type: 'boolean',
        set: function (value) {
          if (!this.attr('activated') && value) {
            this.attr('activated', true);
          }
        }
      }
    },
    activated: false
  });

  /**
   *
   */
  GGRC.Components('lazyRender', {
    tag: 'lazy-render',
    template: '{{#if activated}}<content/>{{/if}}',
    viewModel: viewModel
  });
})(window.can, window.GGRC);
