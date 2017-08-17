/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  GGRC.Components('infoPaneSaveStatus', {
    tag: 'info-pane-save-status',
    viewModel: {
      define: {
        infoPaneSaving: {
          get: function () {
            return this.attr('assessmentSaving') ||
              this.attr('evidencesSaving') ||
              this.attr('commentsSaving') ||
              this.attr('urlsSaving');
          }
        }
      },
      assessmentSaving: false,
      evidencesSaving: false,
      urlsSaving: false,
      commentsSaving: false
    }
  });
})(window.can, window.GGRC);
