/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './collapsible-panel-header.mustache';

(function (can, GGRC) {
  'use strict';

  let tag = 'collapsible-panel-header';
  /**
   * Collapsible Panel component to add collapsing behavior
   */
  GGRC.Components('collapsiblePanelHeader', {
    tag: tag,
    template: template,
    scope: {
      titleIcon: null,
      expanded: null,
      toggle: function () {
        this.attr('expanded', !this.attr('expanded'));
      },
    },
  });
})(window.can, window.GGRC);
