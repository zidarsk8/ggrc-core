/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/
(function (can, GGRC, CMS, $) {
  'use strict';

  var DEFAULT_PAGE_SIZE = 5;
  var DEFAULT_SORT_DIRECTION = 'asc';

  can.Component.extend('mapperResults', {
    tag: 'mapper-results',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-results.mustache'
    ),
    viewModel: {
      paging: {
        current: 1,
        pageSize: DEFAULT_PAGE_SIZE,
        filter: '',
        pageSizeSelect: [5, 10, 15]
      },
      columns: {
        selected: [],
        available: []
      },
      sort: {
        key: '',
        direction: DEFAULT_SORT_DIRECTION
      },
      mapper: null,
      isLoading: false,
      items: [],
      allItems: [],
      allSelected: false,
      baseInstance: null,
      filter: '',
      selected: [],
      refreshItems: false,
      submitCbs: null,
      displayPrefs: null,
      disableColumnsConfiguration: false,
      objectsPlural: false,
      relatedAssessments: {
        state: {},
        instance: null,
        show: false
      },
      init: function () {
        var self = this;
        this.attr('submitCbs').add(this.onSearch.bind(this, true));
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
      setItems: function () {
        var self = this;
        return self.load()
          .then(function (items) {
            self.attr('items', items);
            self.attr('mapper.entries', items.map(function (item) {
              return item.data;
            }));
            self.setColumnsConfiguration();
            self.setRelatedAssessments();
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
      setRelatedAssessments: function () {
        var Model = this.getDisplayModel();
        if (this.useSnapshots()) {
          this.attr('relatedAssessments.show', false);
          return;
        }
        this.attr('relatedAssessments.show',
          !!Model.tree_view_options.show_related_assessments);
      },
      resetSearchParams: function () {
        this.attr('paging.current', 1);
        this.attr('paging.pageSize', DEFAULT_PAGE_SIZE);
        this.attr('sort.key', '');
        this.attr('sort.direction', DEFAULT_SORT_DIRECTION);
      },
      onSearch: function (resetParams) {
        if (resetParams) {
          this.resetSearchParams();
        }
        this.attr('refreshItems', true);
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
              operation: 'relevant',
              id: Number(relevant.filter.id)
            };
          })
          .filter(function (item) {
            return item;
          });
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
            id: this.attr('baseInstance.id'),
            operation: 'relevant'
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
        var selectedItems = can.makeArray(this.attr('selected'));
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
          value.snapshotObject =
            GGRC.Utils.Snapshots.toObject(value);
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
      setItemsDebounced: function () {
        clearTimeout(this.attr('_setItemsTimeout'));
        this.attr('_setItemsTimeout', setTimeout(this.setItems.bind(this)));
      },
      showRelatedAssessments: function (ev) {
        this.attr('relatedAssessments.instance', ev.instance);
        this.attr('relatedAssessments.state.open', true);
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
          this.viewModel.setItemsDebounced();
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
