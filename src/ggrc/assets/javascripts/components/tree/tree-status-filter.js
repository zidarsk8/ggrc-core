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
      set(selected) {
        let statuses = this.attr('filterStates');
        let filter = '';

        statuses.forEach((item) => {
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
  loadTreeStates(modelName) {
    // Get the status list from local storage
    let savedStates = this.attr('displayPrefs')
      .getTreeViewStates(modelName);
    let actualStates = StateUtils.getStatesForModel(modelName);
    let selectedStates = savedStates.filter((state) => {
      return actualStates.includes(state);
    });

    if (selectedStates.length === 0) {
      selectedStates = StateUtils.getDefaultStatesForModel(modelName);
    }

    this.attr('selectedStates', selectedStates);
  },
  saveTreeStates(selectedStates) {
    let stateToSave;
    let filterName = this.attr('widgetId') ||
      this.attr('modelName');

    // in this case we save previous states
    if (!selectedStates) {
      return;
    }

    stateToSave = selectedStates.map((state) => state.value);

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
    inserted() {
      let vm = this.viewModel;
      let options = vm.attr('options');
      let filter = vm.attr('filter');
      let operation = vm.attr('operation');
      let depth = vm.attr('depth');
      let filterName = vm.attr('widgetId') || vm.attr('modelName');
      let filterStates = StateUtils.getStatesForModel(vm.attr('modelName'))
        .map((state) => {
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
        CMS.Models.DisplayPrefs.getSingleton().then((displayPrefs) => {
          vm.attr('displayPrefs', displayPrefs);

          vm.loadTreeStates(filterName);
        });
      }
    },
    'multiselect-dropdown multiselect:closed'(el, ev, selected) {
      ev.stopPropagation();
      this.viewModel.saveTreeStates(selected);
      this.viewModel.dispatch('filter');
    },
    '{viewModel} disabled'() {
      if (this.viewModel.attr('disabled')) {
        this.viewModel.attr('selectedStates', []);
      } else {
        this.viewModel.loadTreeStates(this.viewModel.attr('modelName'));
      }
    },
  },
});
