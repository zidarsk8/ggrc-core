/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/base_objects/repeat-on-summary.mustache');

  GGRC.Components('repeatOnSummary', {
    tag: 'repeat-on-summary',
    template: template,
    viewModel: {
      define: {
        unitText: {
          get: function () {
            var result = '';
            var repeatEvery = this.attr('repeatEvery');
            var unit = GGRC.Workflow.unitOptions
              .find(function (option) {
                return option.value === this.attr('unit');
              }.bind(this));

            if (unit) {
              if (repeatEvery > 1) {
                result += repeatEvery + ' ' + unit.plural;
              } else {
                result += unit.singular;
              }
            }
            return result;
          }
        },
        showRepeatOff: {
          type: 'boolean',
          value: false
        }
      },
      unit: null,
      repeatEvery: null
    }
  });
})(window.can, window.GGRC);
