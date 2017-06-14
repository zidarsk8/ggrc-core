/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function ($, GGRC) {
  'use strict';

  GGRC.Components('clickFilter', {
    tag: 'click-filter',
    viewModel: {
      delay: 300
    },
    events: {
      click: function (el, ev) {
        var $self = $(el);
        var isDisabled = $self.prop('disabled');

        if (isDisabled) {
          ev.stopPropagation();
          return;
        }

        // prevent open of two mappers
        $self.prop('disabled', true);

        setTimeout(function () {
          $self.prop('disabled', false);
        }, this.viewModel.attr('delay'));
      }
    }
  });
})(window.can.$, window.GGRC);
