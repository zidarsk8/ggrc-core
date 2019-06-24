/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './object-selection-item.stache';
import {trigger} from 'can-event';

export default CanComponent.extend({
  tag: 'object-selection-item',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    isSaving: false,
    item: null,
    isDisabled: false,
    isSelected: false,
    isBlocked: false,
    toggleSelection: function (el, isSelected) {
      let event = isSelected ? 'selectItem' : 'deselectItem';
      trigger.call(el[0], event, [this.attr('item')]);
    },
  }),
  events: {
    'input[type="checkbox"] click': function (el, ev) {
      let isSelected = el[0].checked;
      ev.preventDefault();
      ev.stopPropagation();
      this.viewModel
        .toggleSelection(this.element, isSelected);
    },
  },
});
