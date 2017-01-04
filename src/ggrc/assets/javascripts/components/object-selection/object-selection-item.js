/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
      '/components/object-selection/object-selection-item.mustache');

  can.Component.extend({
    tag: 'object-selection-item',
    template: tpl,
    viewModel: {
      isSaving: false,
      objectType: null,
      objectId: null,
      isDisabled: false,
      isSelected: false,
      toggleSelection: function (scope, el, isSelected) {
        var event = isSelected ? 'selectItem' : 'deselectItem';
        can.trigger(el, event, [scope.objectId, scope.objectType]);
      }
    },
    events: {
      'input[type="checkbox"] click': function (el, ev) {
        var isSelected = el[0].checked;
        ev.preventDefault();
        ev.stopPropagation();
        this.viewModel
          .toggleSelection(this.viewModel, this.element, isSelected);
      }
    }
  });
})(window.can, window.GGRC);
