/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/
(function (can, GGRC, CMS, $) {
  'use strict';

  can.Component.extend('mapperResults', {
    tag: 'mapper-results',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-results.mustache'
    ),
    viewModel: {
      paging: {
        current: 1,
        pageSize: 5,
        filter: '',
        pageSizeSelect: [5, 10, 15]
      },
      columns: {
        selected: [],
        available: []
      },
      sort: {
        key: '',
        direction: 'asc'
      },
      mapper: null,
      isLoading: false,
      items: [],
      allItems: [],
      allSelected: false,
      baseInstance: null,
      scopeId: '@',
      scopeType: '@',
      filter: '',
      selected: [],
      refreshItems: false,
      submitCbs: null,
      displayPrefs: null,
      disableColumnsConfiguration: false,
      objectsPlural: false,
      init: function () {
        var self = this;
        this.attr('submitCbs').add(this.onSearch.bind(this));
        CMS.Models.DisplayPrefs.getSingleton().then(function (displayPrefs) {
          self.attr('displayPrefs', displayPrefs);
        });
      },
      destroy: function () {
        this.attr('submitCbs').remove(this.onSearch.bind(this));
      },
      searchOnly: function () {
        return this.attr('mapper.search_only');
      },
      useSnapshots: function () {
        return this.attr('mapper.useSnapshots');
      },
      updatePaging: function (total) {
        var count = Math.ceil(total / this.attr('paging.pageSize'));
        this.attr('paging.total', total);
        this.attr('paging.count', count);
      },
      showNewEntries: function () {
        var self = this;
        var newEntries;
        var sortKey = 'updated_at';
        var sortDirection = 'desc';

        if (this.attr('mapper.newEntries')) {
          newEntries = this.attr('mapper.newEntries').map(function (value) {
            return {
              id: value.id,
              type: value.type,
              data: self.transformValue(value),
              isSelected: true,
              markedSelected: true
            };
          });

          // select new entries
          this.attr('selected').push.apply(this.attr('selected'), newEntries);
        }

        // clear filter
        this.attr('filter', '');
        this.attr('prevSelected', this.attr('selected').slice());

        if (this.attr('sort.key') === sortKey &&
          this.attr('sort.direction') === sortDirection) {
          this.onSearch();
        } else {
          // sort by update date.
          // this action triggers search
          this.attr('sort.key', sortKey);
          this.attr('sort.direction', sortDirection);
        }

        // set current page
        this.attr('paging.current', 1);

        // display results
        this.attr('mapper.afterSearch', true);
      },
      setItems: function () {
        var self = this;
        return self.load()
          .then(function (items) {
            self.attr('items', items);
            self.attr('mapper.entries', items.map(function (item) {
              return item.data;
            }));
            self.setColumnsConfiguration();
            self.attr('isBeforeLoad', false);
          });
      },
      setColumnsConfiguration: function () {
        var columns =
          GGRC.Utils.TreeView.getColumnsForModel(
            this.getDisplayModel().model_singular,
            this.attr('displayPrefs')
          );
        this.attr('columns.available', columns.available);
        this.attr('columns.selected', columns.selected);
        this.attr('disableColumnsConfiguration', columns.disableConfiguration);
      },
      setAdditionalScopeFilter: function () {
        var id = this.attr('baseInstance.scopeObject.id');
        var type = this.attr('baseInstance.scopeObject.type');
        return {
          type: type,
          id: id
        };
      },
      onSearch: function () {
        this.attr('refreshItems', true);
      },
      prepareRelevantFilters: function () {
        var filters;
        var relevantList = this.attr('mapper.relevant');
        var useSnapshots = this.useSnapshots();

        filters = relevantList.attr()
          .map(function (relevant) {
            if (!relevant.value || !relevant.filter) {
              return undefined;
            }
            return {
              type: relevant.filter.type,
              id: Number(relevant.filter.id)
            };
          })
          .filter(function (item) {
            return item;
          });
        // Filter by scope
        if (useSnapshots) {
          if (Number(this.attr('scopeId'))) {
            filters.push({
              type: this.attr('scopeType'),
              id: Number(this.attr('scopeId'))
            });
          } else {
            if (this.attr('baseInstance.scopeObject')) {
              filters.push(this.setAdditionalScopeFilter());
            }
            return filters;
          }
        }
        return filters;
      },
      prepareBaseQuery: function (modelName, paging, filters, ownedFilter) {
        return GGRC.Utils.QueryAPI
          .buildParam(modelName, paging, filters, [], ownedFilter);
      },
      prepareRelatedQuery: function (modelName, ownedFilter) {
        if (!this.attr('baseInstance')) {
          return null;
        }

        return GGRC.Utils.QueryAPI
          .buildRelevantIdsQuery(modelName, {
            filter: this.attr('filter')
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
      loadAllItems: function () {
        this.attr('allItems', this.loadAllItemsIds());
      },
      getQuery: function (queryType, addPaging) {
        var modelName = this.attr('type');
        var useSnapshots = this.useSnapshots();
        var paging = {
          filter: this.attr('filter')
        };
        var filters = this.prepareRelevantFilters();
        var ownedFilter = this.prepareOwnedFilter();
        var query;
        var relatedQuery;

        if (addPaging) {
          paging.current = this.attr('paging.current');
          paging.pageSize = this.attr('paging.pageSize');
          if (this.attr('sort.key')) {
            paging.sortBy = this.attr('sort.key');
            paging.sortDirection = this.attr('sort.direction');
          }
        }

        query = this.prepareBaseQuery(modelName, paging, filters, ownedFilter);
        relatedQuery = this.prepareRelatedQuery(modelName, ownedFilter);
        if (useSnapshots) {
          // Transform Base Query to Snapshot
          query = GGRC.Utils.Snapshots.transformQuery(query);
        }
        // Add Permission check
        query.permissions = 'update';
        query.type = queryType || 'values';

        if (!relatedQuery) {
          return {data: [query]};
        }
        if (useSnapshots) {
          // Transform Related Query to Snapshot
          relatedQuery = GGRC.Utils.Snapshots.transformQuery(relatedQuery);
        }
        return {data: [query, relatedQuery]};
      },
      getModelKey: function () {
        return this.useSnapshots() ?
          CMS.Models.Snapshot.model_singular :
          this.attr('type');
      },
      getModel: function () {
        return CMS.Models[this.getModelKey()];
      },
      getDisplayModel: function () {
        return CMS.Models[this.attr('type')];
      },
      setDisabledItems: function (allItems, relatedIds) {
        if (this.searchOnly() ||
            this.attr('mapper.assessmentGenerator')) {
          return;
        }
        allItems.forEach(function (item) {
          item.isDisabled = relatedIds.indexOf(item.data.id) !== -1;
        });
      },
      setSelectedItems: function (allItems) {
        var selectedItems;

        // get items which were selected before adding of new entries
        if (this.attr('prevSelected') && this.attr('prevSelected').length > 0) {
          this.attr('selected', this.attr('prevSelected').slice());
          this.attr('prevSelected', []);
        }

        selectedItems = can.makeArray(this.attr('selected'));
        allItems.forEach(function (item) {
          item.isSelected =
            selectedItems.some(function (selectedItem) {
              return selectedItem.id === item.id;
            });
          if (item.isSelected) {
            item.markedSelected = true;
          }
        });
      },
      transformValue: function (value) {
        var Model = this.getDisplayModel();
        var useSnapshots = this.useSnapshots();
        if (useSnapshots) {
          value.revision.content =
            Model.model(value.revision.content);
          return value;
        }
        return Model.model(value);
      },
      load: function () {
        var self = this;
        var modelKey = this.getModelKey();
        var dfd = can.Deferred();
        var query = this.getQuery('values', true);
        this.attr('isLoading', true);
        GGRC.Utils.QueryAPI
          .makeRequest(query)
          .done(function (responseArr) {
            var data = responseArr[0];
            var relatedData = responseArr[1];
            var result =
              data[modelKey].values.map(function (value) {
                return {
                  id: value.id,
                  type: value.type,
                  data: self.transformValue(value)
                };
              });
            this.setSelectedItems(result);
            if (relatedData) {
              this.setDisabledItems(result, relatedData[modelKey].ids);
            }
            // Update paging object
            this.updatePaging(data[modelKey].total);
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
      loadAllItemsIds: function () {
        var modelKey = this.getModelKey();
        var dfd = can.Deferred();
        var queryType = 'ids';
        var query = this.getQuery(queryType, false);

        GGRC.Utils.QueryAPI
          .makeRequest(query)
          .done(function (responseArr) {
            var data = responseArr[0];
            var filters = responseArr[1][modelKey].ids;
            var values = data[modelKey][queryType];
            var result = values.map(function (item) {
              return {
                id: item,
                type: modelKey
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
      setItemsDebounced() {
        clearTimeout(this.attr('_setItemsTimeout'));
        this.attr('_setItemsTimeout', setTimeout(this.setItems.bind(this)));
      }
    },
    events: {
      '{viewModel} allSelected': function (scope, ev, allSelected) {
        if (allSelected) {
          this.viewModel.loadAllItems();
        }
      },
      '{viewModel} refreshItems': function (scope, ev, refreshItems) {
        if (refreshItems) {
          this.viewModel.setItems();
          this.viewModel.attr('refreshItems', false);
        }
      },
      '{viewModel.paging} current': function () {
        this.viewModel.setItemsDebounced();
      },
      '{viewModel.paging} pageSize': function () {
        this.viewModel.setItemsDebounced();
      },
      '{viewModel.sort} key': function () {
        this.viewModel.setItemsDebounced();
      },
      '{viewModel.sort} direction': function () {
        this.viewModel.setItemsDebounced();
      },
      '{viewModel} type': function () {
        this.viewModel.attr('items', []);
      },
      '{viewModel.paging} total': function (scope, ev, total) {
        this.viewModel.attr('objectsPlural', total > 1);
      }
    }
  });
})(window.can, window.GGRC, window.CMS, window.jQuery);
