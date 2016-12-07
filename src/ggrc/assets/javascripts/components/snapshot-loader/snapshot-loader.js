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
        pageSizeSelect: [5, 10, 15]
      },
      mapper: null,
      isLoading: false,
      items: [],
      page_loading: false,
      select_state: false,
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
        this.setItems();
      },
      getSelectedType: function () {
        return this.attr('type');
      },
      prepareRelevantFilters: function () {
        var filters;
        var relevantList = this.attr('mapper.relevant');

        filters = _.compact(_.map(relevantList, function (relevant) {
          if (!relevant.value || !relevant.filter) {
            return undefined;
          }
          return {
            type: relevant.filter.type,
            id: relevant.filter.id
          };
        }));
        // Filter by scope
        if (this.attr('mapper.isInScopeObject')) {
          filters.push({
            type: this.attr('scopeType'),
            id: Number(this.attr('scopeId'))
          });
        }
        return filters;
      },
      prepareBaseQuery: function (modelName, filters) {
        return GGRC.Utils.QueryAPI
          .buildParam(modelName, {
            filter: this.attr('term'),
            current: this.attr('paging.current'),
            pageSize: this.attr('paging.pageSize')
          }, filters, {});
      },
      prepareRelatedFilter: function (modelName) {
        return GGRC.Utils.QueryAPI
          .buildRelevantIdsQuery(modelName, {
            filter: this.attr('term')
          }, {
            type: this.attr('baseInstance.type'),
            id: this.attr('baseInstance.id')
          }, {});
      },
      getQuery: function () {
        var contact = this.attr('contact');
        var contactEmail = this.attr('mapper.contactEmail');
        var filters;
        var modelName = this.getSelectedType();
        var params = {};
        var relatedQuery;
        if (contact && contactEmail) {
          params.contact_id = contact.id;
        }

        filters = this.prepareRelevantFilters();
        relatedQuery = this.prepareRelatedFilter(modelName);
        params = this.prepareBaseQuery(modelName, filters);
        params = GGRC.Utils.Snapshots.transformQuery(params);
        params.permissions = 'update';

        relatedQuery = GGRC.Utils.Snapshots.transformQuery(relatedQuery);
        return {data: [params, relatedQuery]};
      },
      load: function () {
        var dfd = can.Deferred();
        var query = this.getQuery();
        this.attr('isLoading', true);
        GGRC.Utils.QueryAPI
          .makeRequest(query)
          .done(function (responseArr) {
            var data = responseArr[0];
            var filters = responseArr[1].Snapshot.ids;
            var values = data.Snapshot.values;
            var result = values.map(function (item) {
              item = GGRC.Utils.Snapshots.toObject(item);
              item.attr('instance', item);
              return item;
            });
            result.forEach(function (item) {
              item.attr('instance.isMapped',
                filters.indexOf(item.attr('id')) > -1);
            });
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
      unselectAll: function (scope, el, ev) {
        ev.preventDefault();

        this.attr('mapper.all_selected', false);
        this.attr('items')
          .forEach(function (item) {
            if (!item.attr('isMapped')) {
              item.attr('isSelected', false);
            }
          });
      },
      selectAll: function (scope, el, ev) {
        ev.preventDefault();
        this.attr('items').forEach(function (item) {
          if (!item.attr('isMapped')) {
            item.attr('isSelected', true);
          }
        });
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
