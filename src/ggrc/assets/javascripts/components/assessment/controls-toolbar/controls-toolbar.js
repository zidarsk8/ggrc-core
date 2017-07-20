/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../../auto-save-form/auto-save-form-actions';

(function (can, GGRC) {
  'use strict';
  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/controls-toolbar/controls-toolbar.mustache');

  can.Component.extend({
    tag: 'assessment-controls-toolbar',
    template: tpl,
    viewModel: {
      instance: null,
      state: {
        open: false
      },
      modalTitle: 'Related Assessments',
      showRelatedResponses: function () {
        this.attr('state.open', true);
      },
      onStateChange: function (event) {
        this.dispatch({
          type: 'onStateChange',
          state: event.state,
          undo: event.undo
        });
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
