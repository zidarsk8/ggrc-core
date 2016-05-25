/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  'use strict';

  GGRC.Components('inlineDatepicker', {
    tag: 'inline-datepicker',
    template: can.view(
      GGRC.mustache_path +
      '/components/inline_edit/datepicker.mustache'
    ),
    scope: {
      context: null
    },
    events: {
      '{scope.context} value': function (scope, ev, val) {
        if (_.isEmpty(val)) {
          return;
        }
        if (!moment(val, 'MM/DD/YYYY', true).isValid()) {
          this.scope.attr('context.value', undefined);
        }
      }
    }
  });
})(window.can, window.can.$);
