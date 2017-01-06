/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('CMS.Models.CycleTaskGroupObjectTask', function () {
  'use strict';

  describe('responseOptionsEditable method', function () {
    var instance;
    var method;  // the method under test
    var Model;
    var origCycleConfig;

    beforeAll(function () {
      Model = CMS.Models.CycleTaskGroupObjectTask;

      // override the Task's cycle attribute config to disable the magic that
      // happens when trying to manually set a mocked Cycle on a Task instance
      origCycleConfig = Model.attributes.cycle;
      delete Model.attributes.cycle;
    });

    afterAll(function () {
      Model.attributes.cycle = origCycleConfig;
    });

    beforeEach(function () {
      instance = new CMS.Models.CycleTaskGroupObjectTask({
        status: 'Assigned',
        cycle: {
          is_current: false
        }
      });

      spyOn(instance.cycle, 'reify').and.returnValue(instance.cycle);

      method = Model.prototype.responseOptionsEditable.bind(instance);
    });

    it('returns false if the Task\'s Cycle is not current for ' +
      'a non-finished task',
      function () {
        var isEditable;
        instance.attr('status', 'InProgress');
        instance.cycle.attr('is_current', false);

        isEditable = method();

        expect(isEditable).toBe(false);
      }
    );

    it('returns false if a Task in a current cycle is completed', function () {
      var END_STATES = ['Verified', 'Finished'];
      var isEditable;

      instance.cycle.attr('is_current', true);

      END_STATES.forEach(function (state) {
        instance.attr('status', state);
        isEditable = method();
        expect(isEditable).toBe(false);
      });
    });

    it('returns true if a Task is in a current cycle and not completed',
      function () {
        var isEditable;
        instance.cycle.attr('is_current', true);
        instance.attr('status', 'InProgress');

        isEditable = method();

        expect(isEditable).toBe(true);
      }
    );
  });
});
