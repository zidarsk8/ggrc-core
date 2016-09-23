/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/mapped-objects/mapped-objects.mustache');
  var tag = 'mapped-objects';
  /**
   * Mapped objects view component
   */
  GGRC.Components('mappedObjects', {
    tag: tag,
    template: tpl,
    scope: {
      isLoading: false,
      mapping: '@',
      parentInstance: null,
      selectedItem: {},
      mappedItems: [],
      filter: null,
      setMappedObjects: function (items) {
        var filterObj = this.attr('filter');
        this.attr('isLoading', false);
        items = filterObj ?
          GGRC.Utils.filters.applyTypeFilter(items, filterObj.serialize()) :
          items;
        this.attr('mappedItems').replace(items);
      },
      load: function () {
        this.attr('isLoading', true);
        this.attr('parentInstance')
          .get_binding(this.attr('mapping'))
          .refresh_instances()
          .then(this.setMappedObjects.bind(this));
      }
    },
    init: function () {
      this.scope.load();
    },
    events: {
      '{scope.parentInstance.related_destinations} length': function () {
        this.scope.load();
      }
    }
  });
})(window.can, window.GGRC);
