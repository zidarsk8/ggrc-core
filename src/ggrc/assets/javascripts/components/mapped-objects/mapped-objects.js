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
      mappedSnapshots: false,
      isLoading: false,
      mapping: '@',
      parentInstance: null,
      selectedItem: {},
      mappedItems: [],
      filter: null,
      filterMappedObjects: function (items) {
        var filterObj = this.attr('filter');
        return filterObj ?
          GGRC.Utils.filters.applyTypeFilter(items, filterObj.attr()) :
          items;
      },
      getBinding: function () {
        return this.attr('parentInstance').get_binding(this.attr('mapping'));
      },
      getShanshotQueryFilters: function () {
        var includeTypes = this.attr('filter.only').attr();
        var excludeTypes = this.attr('filter.exclude').attr();
        var includeFilters = includeTypes.map(function (type) {
          return {
            expression: {
              op: {name: '='},
              left: 'child_type',
              right: type
            }
          };
        });
        var excludeFilters = excludeTypes.map(function (type) {
          return {
            expression: {
              op: {name: '!='},
              left: 'child_type',
              right: type
            }
          };
        });
        return [].concat(includeFilters, excludeFilters);
      },
      getSnapshotQuery: function () {
        var relavantFilters = [{
          type: this.attr('parentInstance.type'),
          id: this.attr('parentInstance.id')
        }];
        var filters = this.getShanshotQueryFilters();
        var query = GGRC.Utils.QueryAPI
          .buildParam('Snapshot', {}, relavantFilters, [], filters);
        return {data: [query]};
      },
      loadSnapshots: function () {
        var dfd = can.Deferred();
        var query = this.getSnapshotQuery();
        this.attr('isLoading', true);
        GGRC.Utils.QueryAPI
          .makeRequest(query)
          .done(function (responseArr) {
            var data = responseArr[0];
            var values = data.Snapshot.values;
            var result = values.map(function (item) {
              item = GGRC.Utils.Snapshots.toObject(item);
              item.attr('instance', item);
              return item;
            });
            dfd.resolve(result);
          })
          .always(function () {
            this.attr('isLoading', false);
          }.bind(this));
        return dfd;
      },
      load: function () {
        var dfd = can.Deferred();
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
        this.attr('mappedItems').replace(
          this.attr('mappedSnapshots') ? this.loadSnapshots() : this.load());
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
