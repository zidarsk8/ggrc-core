/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../cycle-task-group-object-task';
import RefreshQueue from '../../../../models/refresh_queue';
import * as WorkflowHelpers from '../../../../plugins/utils/workflow-utils';
import * as CurrentPageUtils from '../../../../plugins/utils/current-page-utils';

describe('cycle-task-group-object-task component', function () {
  let viewModel;

  beforeEach(function () {
    viewModel = new Component.prototype.viewModel({
      instance: {
        cycle: {},
      },
    });
    viewModel.attr('instance', {
      cycle: {},
    });
  });

  describe('viewModel scope', function () {
    describe('init() method', function () {
      let cycleDfd;

      beforeEach(function () {
        cycleDfd = new can.Deferred();
        spyOn(viewModel, 'loadCycle').and.returnValue(cycleDfd);
      });

      it('calls loadCycle method', function () {
        viewModel.init();
        expect(viewModel.loadCycle).toHaveBeenCalled();
      });

      it('loads workflow after cycle is loaded', function () {
        spyOn(viewModel, 'loadWorkflow');
        cycleDfd.resolve();

        viewModel.init();
        expect(viewModel.loadWorkflow).toHaveBeenCalled();
      });
    });

    describe('loadCycle() method', function () {
      describe('when reified cycle is not empty', function () {
        let trigger;
        let triggerDfd;
        let reifiedCycle;

        beforeEach(function () {
          reifiedCycle = new can.Map({data: 'Data'});
          viewModel.attr('instance.cycle').reify =
            jasmine.createSpy('reify').and.returnValue(reifiedCycle);

          triggerDfd = can.Deferred();
          trigger = spyOn(RefreshQueue.prototype, 'trigger')
            .and.returnValue(triggerDfd);
        });

        it('adds reified cycle to the refresh queue', function () {
          let enqueue = spyOn(RefreshQueue.prototype, 'enqueue')
            .and.returnValue({trigger: trigger});
          viewModel.loadCycle();
          expect(enqueue).toHaveBeenCalledWith(reifiedCycle);
        });

        it('triggers the refresh queue', function () {
          viewModel.loadCycle();
          expect(trigger).toHaveBeenCalled();
        });

        it('returns deferred result', function () {
          let result = viewModel.loadCycle();
          expect(can.isDeferred(result)).toBe(true);
        });

        describe('when the refresh queue was resolved', function () {
          it('returns first result of response', function (done) {
            let data = {data: 'Data'};
            triggerDfd.resolve([data]);
            viewModel.loadCycle().then(function (response) {
              expect(response).toBe(data);
              done();
            });
          });

          it('sets cycle to viewModel', function (done) {
            let data = 'cycle';
            triggerDfd.resolve([data]);
            viewModel.loadCycle().then(function () {
              expect(viewModel.attr('cycle')).toEqual(data);
              done();
            });
          });
        });
      });

      it('returns rejected deferred object', function (done) {
        viewModel.loadCycle().fail(done);
      });
    });

    describe('loadWorkflow() method', () => {
      let cycle;

      beforeEach(function () {
        cycle = new can.Map();
      });

      describe('when a user doesn\'t have enough permissions to get ' +
      'informations about workflow', () => {
        it('builds trimmed workflow object', function () {
          const expectedResult = new can.Map();
          spyOn(viewModel, 'buildTrimmedWorkflowObject')
            .and.returnValue(expectedResult);
          viewModel.loadWorkflow(cycle);
          expect(viewModel.attr('workflow')).toBe(expectedResult);
        });
      });

      describe('when cycle was loaded successfully', function () {
        let trigger;
        let triggerDfd;
        let reifiedObject;

        beforeEach(function () {
          cycle.attr('workflow', {});
          reifiedObject = {};
          cycle.attr('workflow').reify = jasmine.createSpy('reify')
            .and.returnValue(reifiedObject);

          triggerDfd = can.Deferred();
          trigger = spyOn(RefreshQueue.prototype, 'trigger')
            .and.returnValue(triggerDfd);
        });

        describe('before workflow loading', function () {
          let enqueue;

          beforeEach(function () {
            enqueue = spyOn(RefreshQueue.prototype, 'enqueue')
              .and.returnValue({trigger: trigger});
            triggerDfd.resolve();
          });

          it('pushes a workflow to refresh queue', function (done) {
            viewModel.loadWorkflow(cycle)
              .then(function () {
                expect(enqueue).toHaveBeenCalledWith(reifiedObject);
                done();
              });
          });

          it('triggers refresh queue', function (done) {
            viewModel.loadWorkflow(cycle)
              .then(function () {
                expect(trigger).toHaveBeenCalled();
                done();
              });
          });
        });

        describe('after workflow loading', function () {
          it('sets first value of loaded data to workflow field',
            function (done) {
              let data = {data: 'Data'};
              triggerDfd.resolve([data]);
              viewModel.loadWorkflow(cycle)
                .then(function () {
                  expect(viewModel.attr('workflow').serialize()).toEqual(data);
                  done();
                });
            });
        });
      });
    });

    describe('buildTrimmedWorkflowObject() method', () => {
      describe('returns built trimmed workflow object which contains', () => {
        it('a link to the workfolw', function () {
          const link = 'www.example.com';
          let wf;
          spyOn(viewModel, 'buildWorkflowLink').and.returnValue(link);
          wf = viewModel.buildTrimmedWorkflowObject();
          expect(wf.attr('viewLink')).toBe(link);
        });

        it('a workflow title', function () {
          const title = '123';
          let wf;
          viewModel.attr('instance.workflow_title', title);
          wf = viewModel.buildTrimmedWorkflowObject();
          expect(wf.attr('title')).toBe(title);
        });
      });
    });

    describe('buildWorkflowLink() method', () => {
      it('returns link based on workflow id', function () {
        const id = 1;
        const expectedLink = `/workflows/${id}`;
        let result;
        viewModel.attr('instance.workflow', {id});
        result = viewModel.buildWorkflowLink();
        expect(result).toBe(expectedLink);
      });
    });

    describe('onStateChange() method', function () {
      let event;

      beforeEach(function () {
        event = {};
        viewModel.attr('instance', {});
        spyOn(WorkflowHelpers, 'updateStatus');
      });

      it('updates status for cycle task', function () {
        event.state = 'New State';
        viewModel.onStateChange(event);
        expect(WorkflowHelpers.updateStatus).toHaveBeenCalledWith(
          viewModel.attr('instance'),
          event.state
        );
      });
    });

    describe('showLink() method', function () {
      let pageInstance;

      beforeEach(function () {
        pageInstance = spyOn(CurrentPageUtils, 'getPageInstance');
      });

      describe('returns true', function () {
        it('if the workflow is not a page instance', function () {
          let pageInstanceObj = {
            type: 'Type',
          };
          pageInstance.and.returnValue(pageInstanceObj);
          expect(viewModel.showLink()).toBe(true);
        });
      });

      describe('returns false', function () {
        it('if the workflow is a page instance', function () {
          let pageInstanceObj = {
            type: 'Workflow',
          };
          pageInstance.and.returnValue(pageInstanceObj);
          expect(viewModel.showLink()).toBe(false);
        });
      });
    });
  });
});
