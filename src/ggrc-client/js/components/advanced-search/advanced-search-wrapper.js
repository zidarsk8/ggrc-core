/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import canMap from 'can-map';
import canComponent from 'can-component';
import * as StateUtils from '../../plugins/utils/state-utils';
import {getAvailableAttributes} from '../../plugins/utils/tree-view-utils';
import * as AdvancedSearch from '../../plugins/utils/advanced-search-utils';

export default canComponent.extend({
  tag: 'advanced-search-wrapper',
  leakScope: true,
  viewModel: canMap.extend({
    define: {
      hasStatusFilter: {
        get: function () {
          return StateUtils.hasFilter(this.attr('modelName'));
        },
      },
      savedFiltersToApply: {
        set(filters) {
          if (filters) {
            this.attr('filterItems', filters.filterItems || []);
            this.attr('mappingItems', filters.mappingItems || []);
            this.attr('statusItem', filters.statusItem);

            if (filters.modelName && filters.modelDisplayName) {
              this.attr('modelName', filters.modelName);
              this.attr('modelDisplayName', filters.modelDisplayName);
            }

            this.attr('selectedSavedSearchId', filters.savedSearchId);
            this.savedSearchSelected(filters.savedSearchId);
          }
        },
      },
    },
    modelName: null,
    modelDisplayName: null,
    filterItems: [AdvancedSearch.create.attribute()],
    mappingItems: [],
    statusItem: AdvancedSearch.create.state(),
    relevantTo: [],
    selectedSavedSearchId: null,
    savedSearchSelected(savedSearchId) {
      this.dispatch({
        type: 'savedSearchSelected',
        savedSearchId: savedSearchId,
      });
    },
    availableAttributes: function () {
      return getAvailableAttributes(this.attr('modelName'));
    },
    addFilterAttribute: function () {
      let items = this.attr('filterItems');
      if (items.length) {
        items.push(AdvancedSearch.create.operator('AND'));
      }
      items.push(AdvancedSearch.create.attribute());
    },
    addMappingFilter: function () {
      let items = this.attr('mappingItems');
      if (items.length) {
        items.push(AdvancedSearch.create.operator('AND'));
      }
      items.push(AdvancedSearch.create.mappingCriteria());
    },
    resetFilters: function () {
      this.attr('filterItems', [AdvancedSearch.create.attribute()]);
      this.attr('mappingItems', []);
      this.setDefaultStatusItem();
    },
    setDefaultStatusItem: function () {
      if (this.attr('hasStatusFilter')) {
        const defaultStatusItem = AdvancedSearch.setDefaultStatusConfig(
          this.attr('statusItem.value'), this.attr('modelName')
        );
        this.attr('statusItem.value', defaultStatusItem);
      } else {
        this.attr('statusItem', AdvancedSearch.create.state());
      }
    },
    modelNameChanged(ev) {
      this.attr('modelName', ev.modelName);
      this.resetFilters();
    },
  }),
  init: function () {
    this.viewModel.setDefaultStatusItem();
  },
  events: {
    '{viewModel.filterItems} change'() {
      this.viewModel.savedSearchSelected(null);
    },
    '{viewModel.mappingItems} change'() {
      this.viewModel.savedSearchSelected(null);
    },
    '{viewModel.statusItem} change'() {
      this.viewModel.savedSearchSelected(null);
    },
  },
});
