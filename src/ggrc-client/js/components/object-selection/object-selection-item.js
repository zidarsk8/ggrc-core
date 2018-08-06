/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './object-selection-item.mustache';

export default can.Component.extend({
  tag: 'object-selection-item',
  template,
  viewModel: {
    isSaving: false,
    objectType: null,
    objectId: null,
    isDisabled: false,
    isSelected: false,
    toggleSelection: function (scope, el, isSelected) {
      let event = isSelected ? 'selectItem' : 'deselectItem';
      can.trigger(el, event, [scope.objectId, scope.objectType]);
    },
  },
  events: {
    'input[type="checkbox"] click': function (el, ev) {
      let isSelected = el[0].checked;
      ev.preventDefault();
      ev.stopPropagation();
      this.viewModel
        .toggleSelection(this.viewModel, this.element, isSelected);
    },
  },
});
