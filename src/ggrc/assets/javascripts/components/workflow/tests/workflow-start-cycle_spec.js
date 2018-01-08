/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import component from '../workflow-start-cycle';
import helpers from '../workflow-helpers';

describe('GGRC.WorkflowStartCycle', function () {
  var events;
  beforeAll(function () {
    events = component.prototype.events;
  });

  describe('click event handler', function () {
    var handler;
    var workflowMock;
    var generateDfd;

    beforeEach(function () {
      handler = events.click;
      workflowMock = jasmine.createSpyObj('workflow', ['refresh_all']);
      generateDfd = can.Deferred();

      spyOn(GGRC, 'page_instance')
        .and.returnValue(workflowMock);
      spyOn(helpers, 'generateCycle')
        .and.returnValue(generateDfd);
    });

    it('should update TaskGroups when cycle was generated', function () {
      handler();
      generateDfd.resolve();

      expect(helpers.generateCycle).toHaveBeenCalled();
      expect(workflowMock.refresh_all)
                .toHaveBeenCalledWith('task_groups', 'task_group_tasks');
    });

    it('shouldn\'t update TaskGroups when cycle wasn\'t generated',
      function () {
        handler();
        generateDfd.reject();

        expect(helpers.generateCycle).toHaveBeenCalled();
        expect(workflowMock.refresh_all)
          .not.toHaveBeenCalled();
    });
  });
});
