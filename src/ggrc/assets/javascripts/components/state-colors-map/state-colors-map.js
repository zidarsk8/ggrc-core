/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';

  can.Component.extend('stateColorsMap', {
    tag: 'state-colors-map',
    template: '<span style="color: {{color}};">{{state}}</span>',
    viewModel: {
      define: {
        state: {
          type: String,
          value: 'Not Started'
        },
        color: {
          get: function () {
            return this.attr('colorsMap')[this.attr('state')];
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
