/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  var tag = 'object-list-item';
  /**
   * Object List Item component
   */
  can.Component.extend({
    tag: tag,
    viewModel: {
      define: {
        selectionEl: {
          type: String,
          value: ''
        }
      },
      instance: {},
      isSelected: false
    },
    events: {
      '{this.element} click': function (cmpEl, ev) {
        var filter = this.viewModel.attr('selectionEl');
        var el = filter.length ?
          can.$(ev.target).closest(filter, cmpEl) :
          cmpEl;
        if (el.length) {
          can.trigger(el, 'selectItem', [this.viewModel.instance]);
        } else {
          can.trigger(cmpEl, 'deselectItems');
        }
      }
    }
  });
})(window.can, window.GGRC);
