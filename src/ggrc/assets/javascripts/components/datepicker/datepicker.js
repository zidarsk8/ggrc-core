/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  'use strict';

  GGRC.Components('datepicker', {
    tag: 'datepicker',
    template: can.view(
      GGRC.mustache_path +
      '/components/datepicker/datepicker.mustache'
    ),
    scope: {
      date: null,
      format: '@'
    },
    events: {
      inserted: function () {
        this.element.find('.datepicker__input').datepicker();
      }
    }
  });
})(window.can, window.can.$);
