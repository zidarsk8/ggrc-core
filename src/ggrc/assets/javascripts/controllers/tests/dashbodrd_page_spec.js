/*
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.dashboardWidgets', function () {
  var methods;
  var method;

  beforeEach(function () {
    methods = GGRC.Components.get('dashboardWidgets').prototype;
  });

  describe('update_tasks_for_workflow() method', function () {
    var workflow;
    var tasks;

    function generatePreConditions(states, endDates = [], isOverdue = []) {
      var refresh_instances;
      var data = states.map(function (state) {
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
      var states = ['Assigned', 'Assigned',
        'Verified', 'Finished', 'InProgress', 'Declined'];
      var isOverdue = [true, true];
      var expectedResult = {
        task_count: 6,
        assigned: 2,
        assigned_percentage: '33.33',
        completed_percentage: '16.67',
        days_left_for_first_task: 0,
        declined: 1,
        declined_percentage: '16.67',
        finished: 1,
        finished_percentage: '16.67',
        in_progress: 1,
        in_progress_percentage: '16.67',
        over_due: 2,
        over_due_flag: true,
        over_due_percentage: '33.33',
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
