/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/mapped-objects/' +
    'mapped-control-related-objects.mustache');
  var tag = 'assessment-mapped-control-related-objects';
  /**
   * ViewModel for Assessment Mapped Controls Related Objectives and Regulations.
   * @type {can.Map}
   */
  var viewModel = can.Map.extend({
    define: {
      items: {
        value: []
      }
    },
    titleText: '@',
    type: '@'
  });
  /**
   * Specific Wrapper Component to present Controls only inner popover data.
   * Should Load on expand Related Objectives and Regulations
   */
  GGRC.Components('assessmentMappedControlsPopover', {
    tag: tag,
    template: tpl,
    viewModel: viewModel
  });
})(window.can, window.GGRC);
