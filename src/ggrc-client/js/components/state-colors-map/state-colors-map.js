/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, GGRC) {
  'use strict';
  /* Default Sate for Assessment should be 'Not Started' */
  let defaultState = 'Not Started';
  let tpl = '<span class="state-value-dot state-{{suffix}}">{{state}}</span>';

  /**
   * can.Map(ViewModel) presenting behavior of State Colors Map Component
   * @type {can.Map}
   */
  let viewModel = can.Map.extend({
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
    },
  });
  /**
   * Simple Component to add color indication for Assessment State Name
   */
  GGRC.Components('stateColorsMap', {
    tag: 'state-colors-map',
    template: tpl,
    viewModel: viewModel,
  });
})(window.can, window.GGRC);
