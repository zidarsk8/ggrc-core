/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../dashboard_page';

describe('GGRC.Components.dashboardWidgets', function () {
  let methods;
  let method;

  beforeEach(function () {
    methods = Component.prototype;
  });

  describe('update_tasks_for_workflow() method', function () {
    let workflow;
    let tasks;

    function generatePreConditions(states, endDates = [], isOverdue = []) {
      let refresh_instances;
      let data = states.map(function (state) {
        return {
          instance: {status: state},
        };
      });
      endDates.forEach(function (date, i) {
        data[i].instance.end_date = date;
      });
      isOverdue.forEach(function (flag, i) {
        data[i].instance.isOverdue = flag;
      });
      refresh_instances = jasmine.createSpy()
        .and.returnValue(new can.Deferred().resolve(data));
      tasks = {
        refresh_instances: refresh_instances,
      };
      workflow = new can.Map({
        get_binding: jasmine.createSpy().and.returnValue(tasks),
      });
      spyOn($.prototype, 'control').and.returnValue({
        scope: new can.Map(),
      });
    };

    beforeEach(function () {
      method = methods['update_tasks_for_workflow'];
    });

    it('generates tasks percentage and counts into workflow', function (done) {
      let states = ['Assigned', 'Assigned',
        'Verified', 'Finished', 'InProgress', 'Declined'];
      let isOverdue = [true, true];
      let expectedResult = {
        task_count: 6,
        completed_percentage: '16.67',
        days_left_for_first_task: 0,
        finished: 1,
        finished_percentage: '16.67',
        over_due: 2,
        over_due_flag: true,
        task_count: 6,
        verified: 1,
        verified_percentage: '16.67',
      };

      generatePreConditions(states, [], isOverdue);

      method(workflow).then(function () {
        expect(workflow.attr('task_data').serialize())
          .toEqual(jasmine.objectContaining(expectedResult));
        done();
      });
    });
  });
});
