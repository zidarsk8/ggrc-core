/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/simple-popover/simple-popover.mustache');

  can.Component.extend({
    tag: 'simple-popover',
    template: template,
    viewModel: {
      extraCssClass: '@',
      buttonText: '',
      open: false,
      show: function () {
        this.attr('open', true);
      },
      hide: function () {
        this.attr('open', false);
      }
    }
  });
})(window.can, window.GGRC);
