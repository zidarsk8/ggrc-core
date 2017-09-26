/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, moment) {
  'use strict';
  var QueryAPI = GGRC.Utils.QueryAPI;
  var baseCmpName = 'tasks-counter';
  var TASKS_OBJECT_TYPE = 'CycleTaskGroupObjectTask';
  // Temporary Constants => should be replaced by some configuration variables
  var fieldToFilter = 'task due date';
  var valueToFilter = moment().format('YYYY-MM-DD');
  /**
   *  Component to show number of Tasks Owned by Person
   *
   */
  GGRC.Components('tasksCounter', {
    tag: baseCmpName,
    template: can.view(GGRC.mustache_path +
      '/components/tasks-counter/tasks-counter.mustache'),
    viewModel: {
      define: {
        tasksAmount: {
          type: 'number',
          value: 0,
          set: function (newValue) {
            return newValue < 0 ? 0 : newValue;
          }
        },
        hasOverdue: {
          type: 'boolean',
          value: false
        },
        tasksType: {
          type: 'string',
          get: function () {
            return TASKS_OBJECT_TYPE;
          }
        },
        personId: {
          type: 'number',
          set: function (value, setValue) {
            if (!value) {
              return;
            }
            setValue(value);
            this.loadTasks();
          }
        },
        stateCssClass: {
          get: function () {
            if (this.attr('tasksAmount') === 0) {
              return baseCmpName + '__empty-state';
            }
            return this.attr('hasOverdue') ?
              baseCmpName + '__overdue-state' :
              '';
          }
        }
      },
      getQuery: function (type) {
        var ownedFilters = [{
          type: 'Person',
          id: this.attr('personId'),
          operation: 'owned',
          keys: []
        }];
        var overdueQuery;
        var overdueFilter = {
          expression: {
            op: {name: '<'},
            left: fieldToFilter,
            right: valueToFilter
          }};
        overdueQuery = QueryAPI
          .buildParam(type, {}, ownedFilters, null, overdueFilter);
        overdueQuery.type = 'count';
        delete overdueQuery.fields;
        return {
          data: [
            QueryAPI.buildCountParams([type], ownedFilters)[0],
            overdueQuery
          ]
        };
      },
      loadTasks: function () {
        var query = this.getQuery(this.attr('tasksType'));
        return this.requestQuery(query)
          .then(function (results) {
            this.attr('tasksAmount', results.total);
            this.attr('hasOverdue', results.overdue > 0);
          }.bind(this));
      },
      requestQuery: function (query) {
        var dfd = can.Deferred();
        var type = this.attr('tasksType');
        QueryAPI
          .makeRequest(query)
          .done(function (response) {
            var total = response[0][type].total;
            var overdue = response[1][type].total;
            return dfd.resolve({total: total, overdue: overdue});
          })
          .fail(function () {
            return dfd.resolve({total: 0, overdue: 0});
          });
        return dfd;
      }
    },
    events: {
      onModelChange: function (model, event, instance) {
        if (instance instanceof CMS.Models.CycleTaskGroupObjectTask) {
          this.viewModel.loadTasks();
        }
      },
      '{CMS.Models.CycleTaskGroupObjectTask} updated': 'onModelChange',
      '{CMS.Models.CycleTaskGroupObjectTask} destroyed': 'onModelChange',
      '{CMS.Models.CycleTaskGroupObjectTask} created': 'onModelChange'
    }
  });
})(window.can, window.GGRC, moment);
