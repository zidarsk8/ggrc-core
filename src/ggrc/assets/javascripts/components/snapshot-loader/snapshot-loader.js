/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  GGRC.Components('snapshotLoader', {
    tag: 'snapshot-loader',
    template: can.view(
      GGRC.mustache_path +
      '/components/snapshot-loader/snapshot-loader.mustache'
    ),
    scope: {
      paging: {
        current: 1,
        pageSize: 5,
        filter: '',
        pageSizeSelect: [5, 10, 15]
      },
      allSelected: false,
      mapper: null,
      isLoading: false,
      items: [],
      baseInstance: null,
      scopeId: '@',
      scopeType: '@',
      term: '',
      selected: [],
      updatePaging: function (total) {
        var count = Math.ceil(total / this.attr('paging.pageSize'));
        this.attr('paging.total', total);
        this.attr('paging.count', count);
      },
      setItems: function () {
        this.attr('items').replace(this.load());
      },
      onSearch: function () {
        this.clearSelection();
        this.setItems();
      },
      prepareRelevantFilters: function () {
        var filters;
        var relevantList = this.attr('mapper.relevant');

        filters = relevantList.attr()
          .map(function (relevant) {
            if (!relevant.value || !relevant.filter) {
              return undefined;
            }
            return {
              type: relevant.filter.type,
              id: Number(relevant.filter.id)
            };
          }).filter(function (item) {
            return item;
          });
        // Filter by scope
        if (this.attr('mapper.useSnapshots') &&
          Number(this.attr('scopeId'))) {
          filters.push({
            type: this.attr('scopeType'),
            id: Number(this.attr('scopeId'))
          });
        }
        return filters;
      },
      prepareBaseQuery: function (modelName, paging, filters, ownedFilter) {
        return GGRC.Utils.QueryAPI
          .buildParam(modelName, paging, filters, [], ownedFilter);
      },
      prepareRelatedQuery: function (modelName, ownedFilter) {
        return GGRC.Utils.QueryAPI
          .buildRelevantIdsQuery(modelName, {
            filter: this.attr('term')
          }, {
            type: this.attr('baseInstance.type'),
            id: this.attr('baseInstance.id')
          }, [], ownedFilter);
      },
      prepareOwnedFilter: function () {
        var contact = this.attr('contact');
        var contactEmail = this.attr('mapper.contactEmail');
        var operation = 'owned';
        // This property is set to false till filters are not working properly
        var filterIsWorkingProperly = false;

        if (!contact || !contactEmail || !filterIsWorkingProperly) {
          return null;
        }

        return {
          expression: {
            op: {name: operation},
            ids: [String(contact.id)],
            object_name: this.attr('type')
          }
        };
      },
      loadAllItemsIds: function () {
        var dfd = can.Deferred();
        var queryType = 'ids';
        var query = this.getQuery(queryType, false);

        GGRC.Utils.QueryAPI
          .makeRequest(query)
          .done(function (responseArr) {
            var data = responseArr[0];
            var filters = responseArr[1].Snapshot.ids;
            var values = data.Snapshot[queryType];
            var result = values.map(function (item) {
              return {
                id: item,
                type: 'Snapshot'
              };
            });
            // Do not perform extra mapping validation in case Assessment generation
            if (!this.attr('mapper.assessmentGenerator')) {
              result = result.filter(function (item) {
                return filters.indexOf(item.id) < 0;
              });
            }
            dfd.resolve(result);
          }.bind(this))
          .fail(function () {
            dfd.resolve([]);
          });
        return dfd;
      },
      getQuery: function (queryType, addPaging) {
        var modelName = this.attr('type');
        var paging = addPaging ? {
          filter: this.attr('term'),
          current: this.attr('paging.current'),
          pageSize: this.attr('paging.pageSize')
        } : {
          filter: this.attr('term')
        };
        var filters = this.prepareRelevantFilters();
        var ownedFilter = this.prepareOwnedFilter();
        var query =
          this.prepareBaseQuery(modelName, paging, filters, ownedFilter);
        var relatedQuery = this.prepareRelatedQuery(modelName, ownedFilter);
        // Transform Base Query to Snapshot
        query = GGRC.Utils.Snapshots.transformQuery(query);
        // Add Permission check
        query.permissions = 'update';
        query.type = queryType || 'values';
        // Transform Related Query to Snapshot
        relatedQuery = GGRC.Utils.Snapshots.transformQuery(relatedQuery);
        return {data: [query, relatedQuery]};
      },
      load: function () {
        var dfd = can.Deferred();
        var query = this.getQuery('values', true);
        this.attr('isLoading', true);
        GGRC.Utils.QueryAPI
          .makeRequest(query)
          .done(function (responseArr) {
            var data = responseArr[0];
            var filters = responseArr[1].Snapshot.ids;
            var allSelected = this.attr('allSelected');
            var values = data.Snapshot.values;
            var result = values.map(function (item) {
              item = GGRC.Utils.Snapshots.toObject(item);
              item.attr('instance', item);
              item.attr('isSelected', allSelected);
              return item;
            });
            // Do not perform extra mapping validation in case Assessment generation
            if (!this.attr('mapper.assessmentGenerator')) {
              result.forEach(function (item) {
                item.attr('instance.isMapped',
                  filters.indexOf(item.attr('id')) > -1);
              });
            }
            // Update paging object
            this.updatePaging(data.Snapshot.total);
            dfd.resolve(result);
          }.bind(this))
          .fail(function () {
            dfd.resolve([]);
          })
          .always(function () {
            this.attr('isLoading', false);
          }.bind(this));
        return dfd;
      },
      clearSelection: function () {
        this.attr('allSelected', false);
        // Remove all selected items
        this.attr('selected').replace([]);
      },
      unselectAll: function () {
        this.attr('items')
          .forEach(function (item) {
            if (!item.attr('isMapped')) {
              item.attr('isSelected', false);
            }
          });
        this.clearSelection();
      },
      selectAll: function () {
        this.attr('allSelected', true);
        // Add visual Selection to all currently visible items
        this.attr('items').forEach(function (item) {
          if (!item.attr('isMapped')) {
            item.attr('isSelected', true);
          }
        });
        // Replace with actual items loaded from the back-end
        this.attr('selected').replace(this.loadAllItemsIds());
      }
    },
    events: {
      '{scope.paging} current': function () {
        this.scope.setItems();
      },
      '{scope.paging} pageSize': function () {
        this.scope.setItems();
      }
    }
  });
})(window.can, window.can.$);
