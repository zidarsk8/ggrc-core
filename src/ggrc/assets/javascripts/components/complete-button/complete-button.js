/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tag = 'complete-button';
  var tpl = can.view(GGRC.mustache_path +
    '/components/complete-button/complete-button.mustache');
  /**
   * Simple Component to render Complete Button
   */
  can.Component.extend('complete-button', {
    tag: tag,
    template: tpl,
    viewModel: {
      instance: {},
      hasErrors: function () {
        return this.attr('instance._mandatory_msg');
      },
      refreshVerifiers: function () {
        this.attr('instance')
          .get_binding('related_verifiers')
          .refresh_instances()
          .done(function (results) {
            this.attr('hasVerifiers', !!results.length);
          }.bind(this))
          .fail(function () {
            this.attr('hasVerifiers', false);
          }.bind(this));
      }
    },
    init: function () {
      this.viewModel.refreshVerifiers();
    }
  });
})(window.can, window.GGRC);
