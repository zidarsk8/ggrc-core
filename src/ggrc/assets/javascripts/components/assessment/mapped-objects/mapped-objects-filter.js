/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tag = 'assessment-mapped-objects-filter';
  /**
   * Assessment specific filtering mapped objects component
   */
  GGRC.Components('assessmentMappedObjectsFilter', {
    tag: tag,
    scope: {
      mapping: null,
      items: null,
      filter: null,
      filteredItems: [],
      filterFn: function (item) {
        var isControlOnly = this.filter === 'control';
        var isControlType = item.instance.type === 'Control';
        if (isControlOnly) {
          return isControlType;
        }
        return !isControlType;
      },
      setFilteredItems: function (objects) {
        var filteredItems;
        objects = objects.serialize();
        filteredItems = objects
          .map(function (obj) {
            if (this.filterFn(obj)) {
              return obj;
            }
          }.bind(this))
          .filter(function (item) {
            return Boolean(item);
          });

        this.attr('filteredItems').replace(filteredItems);
      }
    },
    events: {
      '{scope} items': function (scope, ev, items) {
        this.scope.setFilteredItems(items);
      }
    }
  });
})(window.can, window.GGRC);
