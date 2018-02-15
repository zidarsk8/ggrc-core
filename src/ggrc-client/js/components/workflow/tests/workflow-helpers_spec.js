/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import workflowHelpers from '../workflow-helpers';

describe('Workflow helpers', () => {
  describe('createCycle() method', () => {
    describe('returns cycle instance which contains', () => {
      let workflow;

      beforeEach(function () {
        workflow = new CMS.Models.Workflow();
        workflow.context = {
          stub: jasmine.createSpy('stub'),
        };
      });

      it('context equals to workflow context stub object', function () {
        const stub = {
          id: 123,
          type: 'Context',
        };
        let context;
        workflow.context.stub.and.returnValue(stub);
        context = workflowHelpers
          .createCycle(workflow)
          .attr('context');
        expect(context.attr()).toEqual(stub);
      });

      it('workflow equals to workflow stub object', function () {
        const stub = {
          id: 123,
          type: 'Workflow',
        };
        let wfStub;
        workflow.attr('id', stub.id);
        wfStub = workflowHelpers
          .createCycle(workflow)
          .attr('workflow');
        expect(wfStub.attr()).toEqual(stub);
      });

      it('autogenerate property equals to true', function () {
        const {autogenerate} = workflowHelpers.createCycle(workflow);
        expect(autogenerate).toBe(true);
      });
    });
  });
});
