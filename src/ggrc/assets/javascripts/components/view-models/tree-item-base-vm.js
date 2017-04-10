/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  if (!GGRC.VM) {
    GGRC.VM = {};
  }

  GGRC.VM.BaseTreeItemVM = can.Map.extend({
    define: {
      expanded: {
        type: Boolean,
        value: false
      }
    },
    instance: null,
    /**
     * Result from mapping
     */
    result: null,
    resultDfd: null,
    limitDepthTree: 0,
    itemSelector: '',
    onExpand: function () {
      var isExpanded = this.attr('expanded');

      this.attr('expanded', !isExpanded);
    },
    onPreview: function (event) {
      var itemSelector = this.attr('itemSelector');
      var selected = event.element.closest(itemSelector);

      this.select(selected);
    },
    select: function ($element) {
      var instance = this.attr('instance');

      if (instance instanceof CMS.Models.Person && !this.attr('result')) {
        this.attr('resultDfd').then(function () {
          can.trigger($element, 'selectTreeItem', [$element, instance]);
        });
      } else {
        can.trigger($element, 'selectTreeItem', [$element, instance]);
      }
    }
  });
})(window.can, window.GGRC);
