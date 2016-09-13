/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/mapped-objects/mapped-controls-popover.mustache');
  var tag = 'assessment-mapped-controls-popover';
  /**
   * Assessment specific mapped objects popover view component
   */
  can.Component.extend({
    tag: tag,
    template: tpl,
    scope: {
      itemData: null
    }
  });
})(window.can, window.GGRC);
