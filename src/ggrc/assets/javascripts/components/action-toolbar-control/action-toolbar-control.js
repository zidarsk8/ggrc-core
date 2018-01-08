/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  'use strict';

  GGRC.Components('actionToolbarControl', {
    tag: 'action-toolbar-control',
    template: '<div class="action-toolbar__controls-item {{disabledCss}}">' +
    '<content></content>' +
    '</div>',
    viewModel: {
      define: {
        disabled: {
          type: 'htmlbool',
          value: false
        },
        disabledCss: {
          type: 'string',
          value: '',
          get: function () {
            return this.attr('disabled') ?
              'action-toolbar__controls-item-disabled' :
              '';
          }
        }
      }
    }
  });
})(window.GGRC);
