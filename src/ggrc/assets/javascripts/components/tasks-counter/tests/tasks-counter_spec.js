/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.TasksCounter', function () {
  'use strict';

  var viewModel;  // the viewModel under test
  var DATE_TO_COMPARE = moment().format('YYYY-MM-DD');
  var TASKS_OBJECT_TYPE = 'CycleTaskGroupObjectTask';
  var testQuery = {
    data: [{
      object_name: TASKS_OBJECT_TYPE,
      type: 'count',
      filters: {
        expression: {
          object_name: 'Person',
          op: {name: 'owned'},
          ids: ['1']
        },
        keys: [],
        order_by: {
          keys: [],
          order: '',
          compare: null
        }
      }
    }, {
      object_name: TASKS_OBJECT_TYPE,
      filters: {
        expression: {
          left: {
            object_name: 'Person',
            op: {name: 'owned'},
            ids: ['1']
          },
          op: {name: 'AND'},
          right: {
            op: {name: '<'},
            left: 'task due date',
            right: DATE_TO_COMPARE
          }
        },
        keys: [null]
      },
      type: 'count'
    }
    ]
  };
  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('tasksCounter');
  });

  describe('initializes default viewModel values', function () {
    it('sets the "tasksAmount" to 0', function () {
      expect(viewModel.attr('tasksAmount')).toEqual(0);
    });

    describe('sets the "tasksAmount" to 0 and ', function () {
      it('doens\'t allow to set it as negative', function () {
        viewModel.attr('tasksAmount', -100);
        expect(viewModel.attr('tasksAmount')).toEqual(0);
      });
    });

    it('sets the "hasOverdue" to 0', function () {
      expect(viewModel.attr('hasOverdue')).toEqual(false);
    });

    it('sets the "tasksType" to CycleTaskGroupObjectTask', function () {
      expect(viewModel.attr('tasksType')).toEqual('CycleTaskGroupObjectTask');
    });

    describe('sets the "tasksType" to ' +
      'CycleTaskGroupObjectTask and ', function () {
      it('doens\'t allow to modify it', function () {
        viewModel.attr('tasksType', 'someDifferent');
        expect(viewModel.attr('tasksType')).toEqual('CycleTaskGroupObjectTask');
      });
    });

    describe('computes "stateCssClass" attribute and sets to ', function () {
      it('"tasks-counter__empty-state", if tasksAmount is 0', function () {
        viewModel.attr('tasksAmount', 0);
        expect(viewModel.attr('stateCssClass'))
          .toEqual('tasks-counter__empty-state');
      });

      it('"tasks-counter__overdue-state",' +
        ' if tasksAmount > 0 and hasOverdue is true', function () {
        viewModel.attr('tasksAmount', 1);
        viewModel.attr('hasOverdue', true);
        expect(viewModel.attr('stateCssClass'))
          .toEqual('tasks-counter__overdue-state');
      });

      it('as empty string,' +
        ' if tasksAmount > 0 and hasOverdue is false', function () {
        viewModel.attr('tasksAmount', 1);
        viewModel.attr('hasOverdue', false);
        expect(viewModel.attr('stateCssClass'))
          .toEqual('');
      });
    });

    describe('on personId attribute update should', function () {
      it('trigger execution of loadTasks method', function () {
        spyOn(viewModel, 'loadTasks');
        viewModel.attr('personId', 1);
        expect(viewModel.attr('personId')).toEqual(1);
        expect(viewModel.loadTasks).toHaveBeenCalled();
      });
    });

    describe('.getQuery() method should', function () {
      it('return QueryAPI object', function () {
        var query;
        viewModel.attr('personId', 1);
        query = viewModel.getQuery('CycleTaskGroupObjectTask');
        expect(JSON.stringify(query)).toBe(JSON.stringify(testQuery));
      });
    });

    describe('.loadTasks() method should', function () {
      it('trigger execution of getQuery and requestQuery methods', function () {
        var results = {
          total: 0,
          overdue: 0
        };
        var resultsDfd = can.Deferred().resolve(results);
        spyOn(viewModel, 'getQuery');
        spyOn(viewModel, 'requestQuery').and.returnValue(resultsDfd);
        viewModel.loadTasks();
        expect(viewModel.getQuery).toHaveBeenCalled();
        expect(viewModel.getQuery)
          .toHaveBeenCalledWith(TASKS_OBJECT_TYPE);
        expect(viewModel.requestQuery).toHaveBeenCalled();
      });

      it('update hasOverdue and tasksAmount properties', function () {
        var results = {
          total: 5,
          overdue: 1
        };
        var resultsDfd = can.Deferred().resolve(results);
        spyOn(viewModel, 'getQuery');
        spyOn(viewModel, 'requestQuery').and.returnValue(resultsDfd);
        viewModel.loadTasks();
        expect(viewModel.getQuery).toHaveBeenCalled();
        expect(viewModel.getQuery)
          .toHaveBeenCalledWith(TASKS_OBJECT_TYPE);
        expect(viewModel.requestQuery).toHaveBeenCalled();
        expect(viewModel.attr('tasksAmount')).toBe(5);
        expect(viewModel.attr('hasOverdue')).toBe(true);
      });
    });
  });
});
