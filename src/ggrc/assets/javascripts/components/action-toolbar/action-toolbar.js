/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  'use strict';

  GGRC.Components('actionToolbar', {
    tag: 'action-toolbar',
    viewModel: {
      showAction: false
    },
    events: {
      '{this.element} mouseenter': function () {
        this.viewModel.attr('showAction', true);
      },
      '{this.element} mouseleave': function () {
        this.viewModel.attr('showAction', false);
      }
    }
  });
})(window.GGRC);
