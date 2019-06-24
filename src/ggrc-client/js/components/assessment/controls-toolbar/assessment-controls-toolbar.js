/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import '../../custom-attributes/custom-attributes-actions';
import '../../object-state-toolbar/object-state-toolbar';
import template from './assessment-controls-toolbar.stache';

export default CanComponent.extend({
  tag: 'assessment-controls-toolbar',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    instance: null,
    verifiers: [],
    isInfoPaneSaving: false,
    isUndoButtonVisible: false,
    currentState: '',
    onStateChange: function (event) {
      this.dispatch({
        type: 'onStateChange',
        state: event.state,
        undo: event.undo,
      });
    },
  }),
});
