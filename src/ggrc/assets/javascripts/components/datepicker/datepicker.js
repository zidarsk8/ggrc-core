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
      format: '@',
      datepicker: null,
      isShown: false,
      onSelect: function (val, ev) {
        this.attr('date', val);
      },
      onFocus: function () {
        this.attr('isShown', true);
      }
    },
    events: {
      inserted: function () {
        var element = this.element.find('.datepicker__calendar');
        var datepicker = element.datepicker({
          altField: this.element.find('.datepicker__input'),
          onSelect: this.scope.onSelect.bind(this.scope)
        }).data('datepicker');
        this.scope.attr('datepicker', datepicker);
      },
      '{window} mousedown': function (el, ev) {
        var isInside = this.element.has(ev.target).length ||
                       this.element.is(ev.target);

        if (this.scope.isShown && !isInside) {
          this.scope.attr('isShown', false);
        }
      }
    }
  });
})(window.can, window.can.$);
