/*
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as StateUtils from '../../plugins/utils/state-utils';

let viewModel = can.Map.extend({
  define: {
    operation: {
      type: String,
      value: 'AND',
    },
    depth: {
      type: Boolean,
      value: false,
    },
    useLocalStorage: {
      type: Boolean,
      value: true,
    },
    selectedStates: {
      type: '*',
      set: function (selected) {
        let statuses = this.attr('filterStates');
        let filter = '';

        statuses.forEach(function (item) {
          item.attr('checked', (selected.indexOf(item.value) > -1));
        });

        if (selected.length && statuses.length !== selected.length) {
          filter = StateUtils.statusFilter(selected, '',
            this.attr('modelName'));
        }

        this.attr('options.filter', filter);
      },
    },
  },
  disabled: false,
  options: {},
  filters: null,
  filterStates: [],
  widgetId: null,
  modelName: null,
  displayPrefs: null,
  loadTreeStates: function (modelName) {
    // Get the status list from local storage
    var savedStates = this.attr('displayPrefs')
      .getTreeViewStates(modelName);
    var actualStates = StateUtils.getStatesForModel(modelName);
    var selectedStates = savedStates.filter(function (state) {
      return actualStates.includes(state);
    });

    if (selectedStates.length === 0) {
      selectedStates = StateUtils.getDefaultStatesForModel(modelName);
    }

    this.attr('selectedStates', selectedStates);
  },
  saveTreeStates: function (selectedStates) {
    var stateToSave;
    var filterName = this.attr('widgetId') ||
      this.attr('modelName');

    // in this case we save previous states
    if (!selectedStates) {
      return;
    }

    stateToSave = selectedStates.map(function (state) {
      return state.value;
    });

    this.attr('selectedStates', stateToSave);

    if (this.attr('useLocalStorage')) {
      this.attr('displayPrefs').setTreeViewStates(filterName, stateToSave);
    }
  },
});

/**
 *
 */
export default GGRC.Components('treeStatusFilter', {
  tag: 'tree-status-filter',
  template: '<content/>',
  viewModel: viewModel,
  events: {
    inserted: function () {
      var vm = this.viewModel;
      var options = vm.attr('options');
      var filter = vm.attr('filter');
      var operation = vm.attr('operation');
      var depth = vm.attr('depth');
      var filterName = vm.attr('widgetId') || vm.attr('modelName');
      var filterStates = StateUtils.getStatesForModel(vm.attr('modelName'))
        .map(function (state) {
          return {
            value: state,
          };
        });

      options.attr('filter', filter);
      options.attr('operation', operation);
      options.attr('depth', depth);
      options.attr('name', 'status');

      if (vm.registerFilter) {
        vm.registerFilter(options);
      }

      vm.attr('filterStates', filterStates);

      if (vm.attr('useLocalStorage')) {
        CMS.Models.DisplayPrefs.getSingleton().then(function (displayPrefs) {
          vm.attr('displayPrefs', displayPrefs);

          vm.loadTreeStates(filterName);
        });
      }
    },
    'multiselect-dropdown multiselect:closed': function (el, ev, selected) {
      ev.stopPropagation();
      this.viewModel.saveTreeStates(selected);
      this.viewModel.dispatch('filter');
    },
    '{viewModel} disabled': function () {
      if (this.viewModel.attr('disabled')) {
        this.viewModel.attr('selectedStates', []);
      } else {
        this.viewModel.loadTreeStates(this.viewModel.attr('modelName'));
      }
    },
  },
});
