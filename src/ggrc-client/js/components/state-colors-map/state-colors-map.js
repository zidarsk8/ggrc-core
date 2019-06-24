/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
/* Default Sate for Assessment should be 'Not Started' */
const defaultState = 'Not Started';

/**
 * CanMap(ViewModel) presenting behavior of State Colors Map Component
 * @type {CanMap}
 */
let viewModel = CanMap.extend({
  define: {
    state: {
      type: 'string',
      value: defaultState,
    },
    suffix: {
      get: function () {
        let state = this.attr('state') || defaultState;
        return state.toLowerCase().replace(/[\s\t]+/g, '');
      },
    },
    verified: {
      get: function (value) {
        return value ? 'verified' : '';
      },
    },
  },
});
/**
 * Simple Component to add color indication for Assessment State Name
 */
export default CanComponent.extend({
  tag: 'state-colors-map',
  view: can.stache(
    '<span class="state-value-dot state-{{suffix}} {{verified}}">' +
    '{{state}}</span>'
  ),
  leakScope: true,
  viewModel,
});
