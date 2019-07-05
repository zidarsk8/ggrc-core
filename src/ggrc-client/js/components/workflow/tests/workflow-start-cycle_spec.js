/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canMap from 'can-map';
import component from '../workflow-start-cycle';
import * as helpers from '../../../plugins/utils/workflow-utils';
import * as CurrentPageUtils from '../../../plugins/utils/current-page-utils';
import * as WidgetsUtils from '../../../plugins/utils/widgets-utils';
import {countsMap as workflowCountsMap} from '../../../apps/workflows';

describe('workflow-start-cycle component', () => {
  let events;

  beforeAll(() => {
    events = component.prototype.events;
  });

  describe('click event handler', () => {
    let handler;
    let workflow;
    let generateDfd;

    beforeEach(() => {
      handler = events.click;
      workflow = new canMap({
        refresh_all: jasmine.createSpy('refresh_all'),
        type: 'Type',
        id: 'ID',
      });
      generateDfd = $.Deferred();

      spyOn(CurrentPageUtils, 'getPageInstance').and.returnValue(workflow);
      spyOn(WidgetsUtils, 'initCounts');
      spyOn(helpers, 'generateCycle').and.returnValue(generateDfd);
    });

    it('should update TaskGroups when cycle was generated', async () => {
      const activeCycleCount = workflowCountsMap.activeCycles;
      workflowCountsMap.activeCycles = 1234;

      handler();
      generateDfd.resolve().then(() => {
        expect(WidgetsUtils.initCounts)
          .toHaveBeenCalledWith([1234], workflow.type, workflow.id);
        workflowCountsMap.activeCycles = activeCycleCount;
      });
    });

    it('should update TaskGroups when cycle was generated', async () => {
      WidgetsUtils.initCounts.and.returnValue(Promise.resolve());
      handler();
      generateDfd.resolve().then(() => {
        expect(helpers.generateCycle).toHaveBeenCalled();
        expect(workflow.refresh_all)
          .toHaveBeenCalledWith('task_groups', 'task_group_tasks');
      });
    });

    it('shouldn\'t update TaskGroups when cycle wasn\'t generated', () => {
      handler();
      generateDfd.reject();

      expect(helpers.generateCycle).toHaveBeenCalled();
      expect(workflow.refresh_all)
        .not.toHaveBeenCalled();
    });
  });
});
