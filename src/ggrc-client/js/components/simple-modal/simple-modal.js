/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './simple-modal.mustache';

(function (can, GGRC) {
  'use strict';

  /**
   * Simple Modal Component is a general abstraction to visualize
   * modal and pop-ups with overlay.
   * Simple Modal can be initialized in any part of the HTML.
   * Simple Modal provides only logic less basic markup. All business logic should be placed on the level of inner components.
   * To simplify styling additional helper CSS classes were created: 'simple-modal__footer', 'simple-modal__body' and 'simple-modal__header'
   */
  can.Component.extend({
    tag: 'simple-modal',
    template: template,
    viewModel: {
      extraCssClass: '@',
      instance: {},
      modalTitle: '',
      replaceContent: false,
      isDisabled: false,
      state: {
        open: false,
      },
      hide: function () {
        this.attr('state.open', false);
      },
      show: function () {
        this.attr('state.open', true);
      },
    },
    helpers: {
      modalWrapper: function (showContent) {
        return (el) => {
          let showHideModal = (val) => {
            if (val) {
              $(el).modal().on('hidden.bs.modal', this.hide.bind(this));
            } else {
              $(el).modal('hide').off('hidden.bs.modal');
            }
          };

          showContent.bind('change', (ev, val) => showHideModal(val));
          showHideModal(showContent);
        };
      },
    },
  });
})(window.can, window.GGRC);
