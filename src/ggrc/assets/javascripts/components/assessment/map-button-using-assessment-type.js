/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  'use strict';

  var tag = 'map-button-using-assessment-type';

  GGRC.Components('mapButtonUsingAssessmentType', {
    tag: tag,
    viewModel: {
      assessmentType: '',
      instance: {},
      onClick: function (el, ev) {
        el.data('type', this.attr('assessmentType'));
        can.trigger(el, 'openMapper', ev);
      }
    },
    events: {
      '.assessment-map-btn click': function (el, ev) {
        this.viewModel.onClick(el, ev);
        ev.preventDefault();
        return false;
      }
    }
  });
})(window.GGRC, window.can);
