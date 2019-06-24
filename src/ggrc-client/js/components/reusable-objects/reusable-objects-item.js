/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './reusable-objects-item.stache';

export default CanComponent.extend({
  tag: 'reusable-objects-item',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    disabled: false,
    reuseAllowed: true,
    instance: {},
    selectedList: [],
    isChecked: false,
    setIsChecked() {
      let instance = this.attr('instance');
      let list = this.attr('selectedList');
      let index = $.makeArray(list).indexOf(instance);

      this.attr('isChecked', index >= 0);
    },
  }),
  events: {
    init() {
      this.viewModel.setIsChecked();
    },
    '{viewModel} isChecked'([viewModel], ev, isChecked) {
      let list = viewModel.attr('selectedList');
      let instance = viewModel.attr('instance');
      let index = list.indexOf(instance);

      if (isChecked && index < 0) {
        list.push(instance);
      } else if (!isChecked) {
        if (index >= 0) {
          list.splice(index, 1);
        }
      }
    },
    '{viewModel.selectedList} length'() {
      this.viewModel.setIsChecked();
    },
  },
});
