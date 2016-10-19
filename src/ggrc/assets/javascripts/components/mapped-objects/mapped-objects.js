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
      filterMappedObjects: function (items) {
        var filterObj = this.attr('filter');
        return filterObj ?
          GGRC.Utils.filters.applyTypeFilter(items, filterObj.serialize()) :
          items;
      },
      getBinding: function () {
        return this.attr('parentInstance').get_binding(this.attr('mapping'));
      },
      load: function () {
        var dfd = new can.Deferred();
        var binding = this.getBinding();

        if (!binding) {
          dfd.resolve([]);
          return dfd;
        }
        // Set Loading Status
        this.attr('isLoading', true);
        binding
          .refresh_instances()
          .done(function (items) {
            dfd.resolve(this.filterMappedObjects(items));
          }.bind(this))
          .fail(function () {
            dfd.resolve([]);
          })
          .always(function () {
            this.attr('isLoading', false);
          }.bind(this));
        return dfd;
      },
      setMappedObjects: function () {
        this.attr('mappedItems').replace(this.load());
      }
    },
    init: function () {
      this.scope.setMappedObjects();
    },
    events: {
      '{scope.parentInstance} change': function () {
        this.scope.setMappedObjects();
      }
    }
  });
})(window.can, window.GGRC);
