/*!
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.tasksSortList', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('tasksSortList');
  });

  describe('compareTasks() method', function () {
    var fakeContext;
    var method;  // the method under test

    function fakeGetTaskDate(instance, type) {
      if (!_.contains(['start', 'end'], type)) {
        throw new Error(
          'The "type" argument must be either "start" or "end", ' +
          'but is ' + type
        );
      }
      return moment.utc(instance[type + '_date']);
    }

    beforeEach(function () {
      fakeContext = new can.Map({
        getTaskDate: fakeGetTaskDate
      });
      method = Component.prototype.compareTasks.bind(fakeContext);
    });

    it('returns a negative number if the 1st task\'s start date comes ' +
      'before the 2nd task\'s start date',
      function () {
        var task = new can.Map({
          instance: {start_date: '2016-05-12'}
        });
        var task2 = new can.Map({
          instance: {start_date: '2016-05-13'}
        });

        var result = method(task, task2);

        expect(typeof result).toEqual('number');
        expect(result).toBeLessThan(0);
      }
    );

    it('returns a positive number if the 1st task\'s start date comes ' +
      'after the 2nd task\'s start date',
      function () {
        var task = new can.Map({
          instance: {start_date: '2016-05-12'}
        });
        var task2 = new can.Map({
          instance: {start_date: '2016-05-11'}
        });

        var result = method(task, task2);

        expect(typeof result).toEqual('number');
        expect(result).toBeGreaterThan(0);
      }
    );

    describe('comparing tasks with the same start dates', function () {
      var task;
      var task2;

      beforeEach(function () {
        task = new can.Map({
          instance: {start_date: '2016-05-12'}
        });
        task2 = new can.Map({
          instance: {start_date: '2016-05-12'}
        });
      });

      it('returns a negative number if the 1st task\'s end date comes ' +
        'before the 2nd task\'s end date',
        function () {
          var result;

          task.instance.attr('end_date', '2016-09-16');
          task2.instance.attr('end_date', '2016-09-17');

          result = method(task, task2);

          expect(typeof result).toEqual('number');
          expect(result).toBeLessThan(0);
        }
      );

      it('returns a positive number if the 1st task\'s end date comes ' +
        'after the 2nd task\'s end date',
        function () {
          var result;

          task.instance.attr('end_date', '2016-09-16');
          task2.instance.attr('end_date', '2016-09-15');

          result = method(task, task2);

          expect(typeof result).toEqual('number');
          expect(result).toBeGreaterThan(0);
        }
      );

      it('returns zero if both tasks\' end dates are the same', function () {
        var result;

        task.instance.attr('end_date', '2016-09-16');
        task2.instance.attr('end_date', '2016-09-16');

        result = method(task, task2);

        expect(typeof result).toEqual('number');
        expect(result).toEqual(0);
      });
    });
  });

  describe('getTaskDate() method', function () {
    var method;  // the method under test

    beforeAll(function () {
      method = Component.prototype.getTaskDate;
    });

    beforeEach(function () {
      jasmine.clock().install();
    });

    afterEach(function () {
      jasmine.clock().uninstall();  //  resets custom date settings
    });

    it('returns task\'s start date if requested and date exists', function () {
      var task = new can.Map({
        start_date: '2016-01-25',
        end_date: '2016-04-18'
      });

      var result = method(task, 'start');
      var expected = moment.utc('2016-01-25');

      expect(moment.isMoment(result)).toBe(true);
      expect(result.isSame(expected)).toBe(true);
    });

    it('returns task\'s end date if requested and date exists', function () {
      var task = new can.Map({
        start_date: '2016-01-25',
        end_date: '2016-04-18'
      });

      var result = method(task, 'end');
      var expected = moment.utc('2016-04-18');

      expect(moment.isMoment(result)).toBe(true);
      expect(result.isSame(expected)).toBe(true);
    });

    it('returns a date relative to the current year if start date ' +
      'is not set on the task',
      function () {
        var expected;
        var result;
        var task;
        var fakeToday = moment.utc('2013-11-20T14:30:52.012Z');

        jasmine.clock().mockDate(fakeToday.toDate());

        task = new can.Map({
          start_date: undefined,
          end_date: '2016-04-18',
          relative_start_day: 31,
          relative_start_month: 12,
          relative_end_day: 28,
          relative_end_month: 8
        });

        result = method(task, 'start');
        expected = moment.utc('2013-12-31');

        expect(moment.isMoment(result)).toBe(true);
        expect(result.isSame(expected)).toBe(true);
      }
    );

    it('returns a date relative to the current date if end date ' +
      'is not set on the task',
      function () {
        var expected;
        var result;
        var task;
        var fakeToday = moment.utc('2013-11-20T14:30:52.012Z');

        jasmine.clock().mockDate(fakeToday.toDate());

        task = new can.Map({
          start_date: '2016-05-19',
          end_date: undefined,
          relative_start_day: 29,
          relative_start_month: 9,
          relative_end_day: 31,
          relative_end_month: 12
        });

        result = method(task, 'end');
        expected = moment.utc('2013-12-31');

        expect(moment.isMoment(result)).toBe(true);
        expect(result.isSame(expected)).toBe(true);
      }
    );

    it('returns the last day of the current month if the task\'s month ' +
      'offset is not set and the days offset would cause a month overflow',
      function () {
        var expected;
        var result;
        var task;
        var fakeToday = moment.utc('2013-09-24T14:30:52.012Z');

        jasmine.clock().mockDate(fakeToday.toDate());

        task = new can.Map({
          start_date: undefined,
          end_date: '2016-04-18',
          relative_start_day: 31,
          relative_start_month: undefined,
          relative_end_day: 31,
          relative_end_month: 12
        });

        result = method(task, 'start');
        expected = moment.utc('2013-09-30');  // no days overflow to October

        expect(moment.isMoment(result)).toBe(true);
        expect(result.isSame(expected)).toBe(true);
      }
    );
  });
});
