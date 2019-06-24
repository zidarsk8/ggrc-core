/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanComponent from 'can-component';
let viewModel = can.Map.extend({
  toState: '',
  changeState: function (newState) {
    this.dispatch({
      type: 'onStateChange',
      state: newState,
    });
  },
});

let events = {
  click: function (element, event) {
    let newState = this.viewModel.attr('toState');
    this.viewModel.changeState(newState);
    event.preventDefault();
  },
};

export default CanComponent.extend({
  tag: 'object-change-state',
  leakScope: true,
  viewModel,
  events,
});
