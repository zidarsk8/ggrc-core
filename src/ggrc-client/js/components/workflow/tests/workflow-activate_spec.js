/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../workflow-activate';
import * as helpers from '../../../plugins/utils/workflow-utils';
import Permission from '../../../permission';
import * as WidgetsUtils from '../../../plugins/utils/widgets-utils';
import {countsMap as workflowCountsMap} from '../../../apps/workflows';

describe('workflow-activate component', function () {
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
      spyOn(helpers, 'redirectToCycle');
    });

    it('should be in waiting state while refresh is in progress',
      function (done) {
        viewModel.repeatOnHandler(workflow);
        expect(viewModel.attr('waiting')).toBe(true);
        done();
      }
    );

    it('should init workflow before refresh the permissions',
      async function (done) {
        await viewModel.repeatOnHandler(workflow);
        expect(viewModel.initWorkflow).toHaveBeenCalledWith(workflow);
        expect(viewModel.initWorkflow).toHaveBeenCalledBefore(
          Permission.refresh
        );
        done();
      }
    );

    it('should refresh permissions', async function (done) {
      await viewModel.repeatOnHandler(workflow);
      expect(Permission.refresh).toHaveBeenCalled();
      expect(Permission.refresh).toHaveBeenCalledBefore(
        viewModel.updateActiveCycleCounts
      );
      done();
    });

    it('should try to update counts for active cycles tab',
      async function (done) {
        await viewModel.repeatOnHandler(workflow);
        expect(viewModel.updateActiveCycleCounts)
          .toHaveBeenCalledWith(workflow);
        done();
      });

    it('should try to refresh TGT after updating counts for active cycles',
      async function (done) {
        await viewModel.repeatOnHandler(workflow);
        expect(workflow.refresh_all)
          .toHaveBeenCalledWith('task_groups', 'task_group_tasks');
        done();
      });

    it('should redirect to WF cycle', async function (done) {
      await viewModel.repeatOnHandler(workflow);
      expect(helpers.redirectToCycle).toHaveBeenCalled();
      done();
    });

    it('should restore button after TGT refresh', async function (done) {
      await viewModel.repeatOnHandler(workflow);
      expect(viewModel.attr('waiting'), false);
      done();
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

    it('refresh passed workflow', async function (done) {
      await viewModel.initWorkflow(workflow);
      expect(workflow.refresh).toHaveBeenCalled();
      expect(workflow.refresh).toHaveBeenCalledBefore(workflow.save);
      done();
    });

    it('sets recurrences to true', async function (done) {
      await viewModel.initWorkflow(workflow);
      expect(workflow.attr('recurrences')).toBe(true);
      done();
    });

    it('sets status to "Active"', async function (done) {
      await viewModel.initWorkflow(workflow);
      expect(workflow.attr('status')).toBe('Active');
      done();
    });

    it('saves workflow', async function (done) {
      await viewModel.initWorkflow(workflow);
      expect(workflow.save).toHaveBeenCalled();
      done();
    });

    it('returns result of save workflow operation', async function (done) {
      const expectedResult = {};
      let result;
      workflow.save.and.returnValue(expectedResult);
      result = await viewModel.initWorkflow(workflow);
      expect(result).toBe(expectedResult);
      done();
    });
  });

  describe('updateActiveCycleCounts() method', () => {
    let workflow;

    beforeEach(function () {
      workflow = {};
      spyOn(WidgetsUtils, 'initCounts');
    });

    it('updates counts for active cycles', function () {
      let activeCycleCount = workflowCountsMap.activeCycles;

      workflowCountsMap.activeCycles = 1234;
      Object.assign(workflow, {
        type: 'Type of workflow',
        id: 4321,
      });
      viewModel.updateActiveCycleCounts(workflow);
      expect(WidgetsUtils.initCounts)
        .toHaveBeenCalledWith([1234], workflow.type, workflow.id);

      workflowCountsMap.activeCycles = activeCycleCount;
    });

    it('returns result of update operation', async function (done) {
      const expectedResult = {};
      let result;
      WidgetsUtils.initCounts.and.returnValue(expectedResult);
      result = await viewModel.updateActiveCycleCounts(workflow);
      expect(result).toBe(expectedResult);
      done();
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
      async function (done) {
        await viewModel.repeatOffHandler(workflow);
        expect(helpers.generateCycle).toHaveBeenCalledWith(workflow);
        expect(helpers.generateCycle).toHaveBeenCalledBefore(
          workflow.refresh
        );
        done();
      });

    it('refreshes workflow', async function (done) {
      await viewModel.repeatOffHandler(workflow);
      expect(workflow.refresh).toHaveBeenCalled();
      done();
    });

    it('sets active status for passed workflow', async function (done) {
      await viewModel.repeatOffHandler(workflow);
      expect(workflow.attr('status')).toBe('Active');
      done();
    });

    it('saves workflow', async function (done) {
      await viewModel.repeatOffHandler(workflow);
      expect(workflow.save).toHaveBeenCalled();
      done();
    });

    it('should restore button after workflow saving', async function (done) {
      await viewModel.repeatOffHandler(workflow);
      expect(viewModel.attr('waiting'), false);
      done();
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
});
