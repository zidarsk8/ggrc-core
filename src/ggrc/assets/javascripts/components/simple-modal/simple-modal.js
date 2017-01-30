/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/simple-modal/simple-modal.mustache');
  var baseCls = 'simple-modal';

  can.Component.extend({
    tag: 'simple-modal',
    template: tpl,
    viewModel: {
      extraCssClass: '@',
      instance: null,
      modalTitle: '',
      state: {
        open: false
      },
      hide: function () {
        this.attr('state.open', false);
      },
      show: function () {
        this.attr('state.open', true);
      }
    }
  });
})(window.can, window.GGRC);
