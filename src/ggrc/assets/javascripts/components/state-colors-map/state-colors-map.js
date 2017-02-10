/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';
  /* Default Sate for Assessment should be 'Not Started' */
  var defaultState = 'Not Started';
  /**
   * Simple Component to add color indication for Assessment State Name
   */
  can.Component.extend('stateColorsMap', {
    tag: 'state-colors-map',
    template: '<span style="color: {{color}};">{{state}}</span>',
    viewModel: {
      define: {
        state: {
          type: String,
          value: defaultState
        },
        color: {
          get: function () {
            var color = this.attr('colorsMap')[this.attr('state')];
            if (!color) {
              console.warn('State of the Object is not defined in Color Map: ',
                this.attr('state'));
            }
            /* Set default 'Not Started' State Color in case incorrect state is provided */
            return color || this.attr('colorsMap')[defaultState];
          }
        },
        colorsMap: {
          type: '*',
          value: function () {
            return {
              'Not Started': '#bdbdbd',
              'In Progress': '#ffab40',
              'Ready for Review': '#1378bb',
              Verified: '#333',
              Completed: '#8bc34a'
            };
          }
        }
      }
    }
  });
})(window.can);
