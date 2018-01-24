/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  let template = can.view(GGRC.mustache_path +
    '/base_objects/repeat-on-summary.mustache');

  GGRC.Components('repeatOnSummary', {
    tag: 'repeat-on-summary',
    template: template,
    viewModel: {
      define: {
        unitText: {
          get: function () {
            let result = '';
            let repeatEvery = this.attr('repeatEvery');
            let unit = _.find(GGRC.Workflow.unitOptions, function (option) {
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
          },
        },
        hideRepeatOff: {
          type: 'boolean',
          value: true,
        },
      },
      unit: null,
      repeatEvery: null,
    },
  });
})(window.can, window.GGRC);
