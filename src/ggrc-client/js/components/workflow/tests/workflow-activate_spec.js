/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../workflow-activate';
import helpers from '../workflow-helpers';
import Permission from '../../../permission';
import * as CurrentPageUtils from '../../../plugins/utils/current-page-utils';

describe('GGRC.WorkflowActivate', function () {
  let viewModel;

  beforeEach(function () {
    viewModel = getComponentVM(Component);
  });

  describe('activateWorkflow() method', () => {
    beforeEach(function () {
      viewModel.attr('instance', {});
    });

    describe('when workflow is "Repeat On"', () => {
      it('calls repeatOnHandler method', function () {
        spyOn(viewModel, 'repeatOnHandler');
        viewModel.attr('instance.unit', 'weekly');
        viewModel.activateWorkflow();
        expect(viewModel.repeatOnHandler).toHaveBeenCalled();
      });
    });

    describe('when workflow is "Repeat Off"', () => {
      it('calls repeatOffHandler method', function () {
        spyOn(viewModel, 'repeatOffHandler');
        viewModel.attr('instance.unit', null);
        viewModel.activateWorkflow();
        expect(viewModel.repeatOffHandler).toHaveBeenCalled();
      });
    });
  });

  describe('repeatOnHandler() method', () => {
    let workflow;

    beforeEach(function () {
      workflow = new can.Map();
      workflow.refresh_all = jasmine.createSpy('refresh_all');
      spyOn(viewModel, 'initWorkflow');
      spyOn(Permission, 'refresh');
      spyOn(viewModel, 'updateActiveCycleCounts');
      spyOn(viewModel, 'redirectToFirstCycle');
    });

    it('should be in waiting state while refresh is in progress', function () {
      viewModel.repeatOnHandler();
      expect(viewModel.attr('waiting')).toBe(true);
    });

    it('should init workflow before refresh the permissions', function () {
      viewModel.repeatOnHandler(workflow);
      expect(viewModel.initWorkflow).toHaveBeenCalledWith(workflow);
    });

    it('should refresh permissions', async function () {
      await viewModel.repeatOnHandler(workflow);
      expect(Permission.refresh).toHaveBeenCalled();
      expect(Permission.refresh).toHaveBeenCalledBefore(
        viewModel.updateActiveCycleCounts
      );
    });

    it('should try to update counts for active cycles tab', async function () {
      await viewModel.repeatOnHandler(workflow);
      expect(viewModel.updateActiveCycleCounts)
        .toHaveBeenCalledWith(workflow);
    });

    it('should try to refresh TGT after updating counts for active cycles',
      async function () {
        await viewModel.repeatOnHandler(workflow);
        expect(workflow.refresh_all)
          .toHaveBeenCalledWith('task_groups', 'task_group_tasks');
      });

    it('should redirect to WF cycle', async function () {
      await viewModel.repeatOnHandler(workflow);
      expect(viewModel.redirectToFirstCycle)
        .toHaveBeenCalledWith(workflow);
    });

    it('should restore button after TGT refresh', async function () {
      await viewModel.repeatOnHandler(workflow);
      expect(viewModel.attr('waiting'), false);
    });

    it('should restore button when initWorkflow fails', async function (done) {
      viewModel.initWorkflow.and.returnValue(Promise.reject());
      try {
        await viewModel.repeatOnHandler(workflow);
      } catch (err) {
        expect(viewModel.attr('waiting')).toBe(false);
        done();
      }
    });

    it('should restore button when permission refresh fails',
      async function (done) {
        Permission.refresh.and.returnValue(Promise.reject());
        try {
          await viewModel.repeatOnHandler(workflow);
        } catch (err) {
          expect(viewModel.attr('waiting')).toBe(false);
          done();
        }
      });

    it('should restore button when counts update fails', async function (done) {
      viewModel.updateActiveCycleCounts.and.returnValue(Promise.reject());
      try {
        await viewModel.repeatOnHandler(workflow);
      } catch (err) {
        expect(viewModel.attr('waiting')).toBe(false);
        done();
      }
    });

    it('should restore button when TG refresh fails', async function (done) {
      workflow.refresh_all.and.returnValue(Promise.reject());
      try {
        await viewModel.repeatOnHandler(workflow);
      } catch (err) {
        expect(viewModel.attr('waiting')).toBe(false);
        done();
      }
    });
  });

  describe('initWorkflow() method', () => {
    let workflow;

    beforeEach(function () {
      workflow = new can.Map({});
      Object.assign(workflow, {
        refresh: jasmine.createSpy('refresh'),
        save: jasmine.createSpy('save'),
      });
    });

    it('refresh passed workflow', async function () {
      await viewModel.initWorkflow(workflow);
      expect(workflow.refresh).toHaveBeenCalled();
      expect(workflow.refresh).toHaveBeenCalledBefore(workflow.save);
    });

    it('sets recurrences to true', async function () {
      await viewModel.initWorkflow(workflow);
      expect(workflow.attr('recurrences')).toBe(true);
    });

    it('sets status to "Active"', async function () {
      await viewModel.initWorkflow(workflow);
      expect(workflow.attr('status')).toBe('Active');
    });

    it('saves workflow', async function () {
      await viewModel.initWorkflow(workflow);
      expect(workflow.save).toHaveBeenCalled();
    });

    it('returns result of save workflow operation', async function () {
      const expectedResult = {};
      let result;
      workflow.save.and.returnValue(expectedResult);
      result = await viewModel.initWorkflow(workflow);
      expect(result).toBe(expectedResult);
    });
  });

  describe('updateActiveCycleCounts() method', () => {
    let originalExt;
    let extension;
    let workflow;

    beforeEach(function () {
      originalExt = GGRC.extensions;
      workflow = {};
      extension = {
        name: 'workflows',
        countsMap: {},
      };
      GGRC.extensions = [extension];
      spyOn(CurrentPageUtils, 'initCounts');
    });

    afterEach(function () {
      GGRC.extensions = originalExt;
    });

    it('updates counts for active cycles', function () {
      extension.countsMap.activeCycles = 1234;
      Object.assign(workflow, {
        type: 'Type of workflow',
        id: 4321,
      });
      viewModel.updateActiveCycleCounts(workflow);
      expect(CurrentPageUtils.initCounts).toHaveBeenCalledWith([
        extension.countsMap.activeCycles
      ], workflow.type, workflow.id);
    });

    it('returns result of update operation', async function () {
      const expectedResult = {};
      let result;
      CurrentPageUtils.initCounts.and.returnValue(expectedResult);
      result = await viewModel.updateActiveCycleCounts(workflow);
      expect(result).toBe(expectedResult);
    });
  });

  describe('redirectToFirstCycle() method', () => {
    let workflow;

    beforeEach(function () {
      workflow = new can.Map({cycles: []});
      spyOn(helpers, 'redirectToCycle');
    });

    it('redirects to first workflow cycle', function () {
      const cycleStub = new can.Map({
        id: 123,
        type: 'Cycle',
      });
      workflow.attr('cycles').push(cycleStub);
      viewModel.redirectToFirstCycle(workflow);
      expect(helpers.redirectToCycle).toHaveBeenCalledWith(cycleStub);
    });
  });

  describe('repeatOffHandler() method', () => {
    let workflow;

    beforeEach(function () {
      workflow = new can.Map();
      workflow.refresh = jasmine.createSpy('refresh');
      workflow.save = jasmine.createSpy('save');
      spyOn(helpers, 'generateCycle');
    });

    it('should be in waiting state while refresh is in progress', function () {
      viewModel.repeatOffHandler(workflow);
      expect(viewModel.attr('waiting')).toBe(true);
    });

    it('generates cycle for passed workflow before workflow refreshing',
      async function () {
        await viewModel.repeatOffHandler(workflow);
        expect(helpers.generateCycle).toHaveBeenCalledWith(workflow);
        expect(helpers.generateCycle).toHaveBeenCalledBefore(
          workflow.refresh
        );
      });

    it('refreshes workflow', async function () {
      await viewModel.repeatOffHandler(workflow);
      expect(workflow.refresh).toHaveBeenCalled();
    });

    it('sets active status for passed workflow', async function () {
      await viewModel.repeatOffHandler(workflow);
      expect(workflow.attr('status')).toBe('Active');
    });

    it('saves workflow', async function () {
      await viewModel.repeatOffHandler(workflow);
      expect(workflow.save).toHaveBeenCalled();
    });

    it('should restore button after workflow saving', async function () {
      await viewModel.repeatOffHandler(workflow);
      expect(viewModel.attr('waiting'), false);
    });

    it('should restore button when cycle generating fails',
      async function (done) {
        helpers.generateCycle.and.returnValue(Promise.reject());
        try {
          await viewModel.repeatOffHandler(workflow);
        } catch (err) {
          expect(viewModel.attr('waiting')).toBe(false);
          done();
        }
      });

    it('should restore button when workflow refreshing fails',
      async function (done) {
        workflow.refresh.and.returnValue(Promise.reject());
        try {
          await viewModel.repeatOffHandler(workflow);
        } catch (err) {
          expect(viewModel.attr('waiting')).toBe(false);
          done();
        }
      });

    it('should restore button when workflow saving fails',
      async function (done) {
        workflow.save.and.returnValue(Promise.reject());
        try {
          await viewModel.repeatOffHandler(workflow);
        } catch (err) {
          expect(viewModel.attr('waiting')).toBe(false);
          done();
        }
      });
  });

  describe('canActivateWorkflow() method', () => {
    let workflow;
    let tgs;

    beforeEach(function () {
      tgs = [];
      workflow = {
        task_groups: {
          reify: jasmine.createSpy('reify').and.returnValue(tgs),
        },
      };
    });

    it('calls reify method for TGs', function () {
      viewModel.canActivateWorkflow(workflow);
      expect(workflow.task_groups.reify).toHaveBeenCalled();
    });

    it('returns false if there are no task groups', function () {
      const result = viewModel.canActivateWorkflow(workflow);
      expect(result).toBe(false);
    });

    it('returns false if some of task group does not have task group tasks',
      function () {
        let result;
        tgs.push(...[
          {task_group_tasks: [{}]},
          {task_group_tasks: []},
        ]);
        result = viewModel.canActivateWorkflow(workflow);
        expect(result).toBe(false);
      });

    it('returns true if each task group has at least one task group task',
      function () {
        let result;
        tgs.push(...[
          {task_group_tasks: [{}]},
          {task_group_tasks: [{}]},
        ]);
        result = viewModel.canActivateWorkflow(workflow);
        expect(result).toBe(true);
      });
  });
});
