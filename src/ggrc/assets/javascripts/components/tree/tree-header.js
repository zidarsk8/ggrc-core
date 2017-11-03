/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../sortable-column/sortable-column';
import template from './templates/tree-header.mustache';
import {createSelectedColumnsMap} from '../../plugins/utils/tree-view-utils';

(function (can, GGRC) {
  'use strict';

  var viewModel = can.Map.extend({
    define: {
      cssClasses: {
        type: String,
        get: function () {
          var classes = [];

          if (this.isActiveActionArea()) {
            classes.push('active-action-area');
          }

          return classes.join(' ');
        }
      },
      selectableSize: {
        type: Number,
        get: function () {
          var attrCount = this.attr('selectedColumns').length;
          var result = 3;

          if (attrCount < 4) {
            result = 1;
          } else if (attrCount < 7) {
            result = 2;
          }
          return result;
        }
      }
    },
    model: null,
    columns: {},
    selectedColumns: [],
    availableColumns: [],
    disableConfiguration: null,
    mandatory: [],
    orderBy: {},
    sortingInfo: null,
    /**
     * Dispatches the event with names of selected columns.
     *
     * @fires updateColumns
     */
    setColumns: function () {
      var selectedNames = [];

      can.each(this.attr('columns'), function (v, k) {
        if (v) {
          selectedNames.push(k);
        }
      });

      this.dispatch({
        type: 'updateColumns',
        columns: selectedNames
      });
    },
    onChange: function (attr) {
      var columns = this.attr('columns').serialize();

      columns[attr.attr_name] = !columns[attr.attr_name];
      this.columns.attr(columns);
    },
    onOrderChange() {
      const field = this.attr('orderBy.field');
      const sortDirection = this.attr('orderBy.direction');

      this.dispatch({
        type: 'sort',
        field,
        sortDirection,
      });
    },
    initializeColumns: function () {
      var selectedColumns = this.attr('selectedColumns');
      var availableColumns = this.attr('availableColumns');
      var columns;

      if (selectedColumns.length && availableColumns.length) {
        columns = createSelectedColumnsMap(availableColumns, selectedColumns);

        this.attr('columns', columns);
      }
    },
    isActiveActionArea: function () {
      var modelName = this.attr('model').shortName;

      return modelName === 'CycleTaskGroupObjectTask' || modelName === 'Cycle';
    },
    init: function () {
      this.initializeColumns();
    }
  });

  GGRC.Components('treeHeader', {
    tag: 'tree-header',
    template: template,
    viewModel: viewModel,
    events: {
      '{viewModel} availableColumns': function () {
        this.viewModel.initializeColumns();
      },
      '{viewModel} selectedColumns': function () {
        this.viewModel.initializeColumns();
      },
      '{viewModel.orderBy} change'() {
        this.viewModel.onOrderChange();
      },
    },
  });
})(window.can, window.GGRC);
