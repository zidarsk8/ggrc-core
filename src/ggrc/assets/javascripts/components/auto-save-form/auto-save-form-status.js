/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC) {
  'use strict';

  var ALL_SAVED_TEXT = 'All changes saved';
  var IS_SAVING_TEXT = 'Saving...';

  GGRC.Components('autoSaveFormStatus', {
    tag: 'auto-save-form-status',
    template: '{{formStatusText}}<content></content>',
    viewModel: {
      define: {
        formSaving: {
          type: 'boolean',
          value: false
        },
        formStatusText: {
          type: 'string',
          get: function () {
            return this.attr('formSaving') ? IS_SAVING_TEXT : ALL_SAVED_TEXT;
          }
        }
      }
    }
  });
})(window.can, window.GGRC);
