/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.ObjectCounter', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('ObjectCounter');
  });

  describe('initializing scope values', function () {
    var origCounters;
    var html;
    var $componentRoot;  // component instance's root element

    beforeEach(function () {
      var mustacheContext;
      var renderer;
      var template;
      var $body = $('body');

      origCounters = GGRC.counters;
      GGRC.counters = {
        user_task_count: 7,
        user_overdue_task_count: 2
      };

      template = [
        '<object-counter',
        '  counter="user_task_count"',
        '  counter-overdue="user_overdue_task_count"',
        '  search-keys="user_id;verbose"',
        '  search-values="42;true"',
        '  model-name="CycleTaskGroupObjectTask"',
        '  >',
        '</object-counter>'
      ].join('');

      mustacheContext = {};

      renderer = can.view.mustache(template);
      html = renderer(mustacheContext);
      $body.append(html);

      $componentRoot = $body.children('object-counter');
    });

    afterEach(function () {
      $componentRoot.remove();
      GGRC.counters = origCounters;
    });

    it('sets the task count to the global counter value', function () {
      var scope = $componentRoot.scope();
      expect(scope.count).toEqual(7);
    });

    it('sets the overdue task count to the global counter value', function () {
      var scope = $componentRoot.scope();
      expect(scope.overdueCount).toEqual(2);
    });
  });

  describe('updateCount() method', function () {
    var dfdFindAll;
    var origCurrentUser;
    var scope;
    var updateCount;

    beforeAll(function () {
      origCurrentUser = GGRC.current_user;
      GGRC.current_user = {
        id: 117,
        name: 'John Doe'
      };
    });

    afterAll(function () {
      GGRC.current_user = origCurrentUser;
    });

    beforeEach(function () {
      jasmine.clock().install();

      scope = new can.Map({
        modelName: 'CycleTaskGroupObjectTask',
        searchKeys: 'user_id;verbose',
        searchValues: '42;true',
        _getValue: {}
      });

      // The updateCount method is throttled, thus we need to cancel any
      // delayed invocation timers in order to put it into a "fresh" state,
      // so that its the next call in a test case will be executed immediately.
      updateCount = Component.prototype.scope.updateCount;
      updateCount.cancel();
      updateCount = updateCount.bind({scope: scope});

      dfdFindAll = new can.Deferred();
      spyOn(CMS.Models.CycleTaskGroupObjectTask, 'findAll')
        .and.returnValue(dfdFindAll.promise());
    });

    afterEach(function () {
      jasmine.clock().uninstall();
    });

    it('sets overdue tasks counter to zero if no objects retrieved',
      function () {
        scope.attr('overdueCount', 99);
        updateCount();
        dfdFindAll.resolve([]);
        expect(scope.overdueCount).toEqual(0);
      }
    );

    it('sets the tasks counter to the number of tasks that are overdue',
      function () {
        var fetchedObjects;
        var fakeToday = moment('2016-11-20 10:16:23Z');

        jasmine.clock().mockDate(fakeToday.toDate());

        fetchedObjects = [
          new can.Map({
            end_date: new Date('2017-01-15T08:12:00Z')
          }),
          new can.Map({
            end_date: new Date('2016-11-18T19:45:07Z')  // overdue
          }),
          new can.Map({
            end_date: new Date('2018-05-07T12:22:09Z')
          }),
          new can.Map({
            end_date: new Date('2016-09-27T15:00:00Z')  // overdue
          }),
          new can.Map({
            end_date: new Date('2016-12-31T23:59:59Z')
          })
        ];
        scope.attr('overdueCount', 99);

        updateCount();
        dfdFindAll.resolve(fetchedObjects);

        expect(scope.overdueCount).toEqual(2);
      }
    );

    it('considers only the date part when determining if an object is overdue',
      function () {
        var fetchedObjects;
        var fakeToday = moment('2016-11-20 10:16:23.000Z');

        jasmine.clock().mockDate(fakeToday.toDate());

        fetchedObjects = [
          new can.Map({
            end_date: new Date('2016-11-20T07:55:35.000Z')
          }),
          new can.Map({
            end_date: new Date('2016-11-20T10:16:22.999Z')
          }),
          new can.Map({
            end_date: new Date('2016-11-20T10:16:23.000Z')
          }),
          new can.Map({
            end_date: new Date('2016-11-20T23:59:59.999Z')
          }),
          new can.Map({
            end_date: new Date('2016-11-19T23:59:59.999Z')  // overdue
          })
        ];
        scope.attr('overdueCount', 99);

        updateCount();
        dfdFindAll.resolve(fetchedObjects);

        expect(scope.overdueCount).toEqual(1);
      }
    );

    it('treats objects with undefined end date as NOT overdue', function () {
      var fetchedObjects;
      var fakeToday = moment('2016-11-20 10:16:23.000Z');

      jasmine.clock().mockDate(fakeToday.toDate());

      fetchedObjects = [
        new can.Map({
          end_date: undefined
        })
      ];
      scope.attr('overdueCount', 99);

      updateCount();
      dfdFindAll.resolve(fetchedObjects);

      expect(scope.overdueCount).toEqual(0);
    });
  });
});
