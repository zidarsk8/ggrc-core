/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../cycle-task-group-object-task';
import * as WorkflowHelpers from '../../../../plugins/utils/workflow-utils';
import * as CurrentPageUtils from '../../../../plugins/utils/current-page-utils';
import {getComponentVM} from '../../../../../js_specs/spec_helpers';
import Permission from '../../../../permission';

describe('cycle-task-group-object-task component', function () {
  let viewModel;

  beforeEach(function () {
    viewModel = getComponentVM(Component);
  });

  describe('isEditDenied get() method', () => {
    beforeEach(function () {
      spyOn(Permission, 'is_allowed_for');
    });

    it('returns false if there is access to edit instance', () => {
      Permission.is_allowed_for.and.returnValue(true);
      viewModel.attr('instance', {is_in_history: false});

      expect(viewModel.attr('isEditDenied')).toBe(false);
    });

    describe('returns true', () => {
      it('if there are no "update "permissions for the instance', function () {
        Permission.is_allowed_for.and.returnValue(false);

        const result = viewModel.attr('isEditDenied');

        expect(Permission.is_allowed_for)
          .toHaveBeenCalledWith('update', viewModel.attr('instance'));
        expect(result).toBe(true);
      });

      it('if the instance is in history', function () {
        Permission.is_allowed_for.and.returnValue(true);
        viewModel.attr('instance', {is_in_history: true});

        expect(viewModel.attr('isEditDenied')).toBe(true);
      });
    });
  });

  describe('showWorfklowLink get() method', () => {
    let getPageType;

    beforeEach(function () {
      getPageType = spyOn(CurrentPageUtils, 'getPageType');
    });

    it('returns true if page type is not equal to "Workflow"', function () {
      getPageType.and.returnValue('NotWorkflow');
      expect(viewModel.attr('showWorkflowLink')).toBe(true);
    });

    it('returns false if page type equals to "Workflow"', function () {
      getPageType.and.returnValue('Workflow');
      expect(viewModel.attr('showWorkflowLink')).toBe(false);
    });
  });

  describe('workflowLink get() method', () => {
    it('returns link to workflow, which is relevant to instance', () => {
      const id = 1234567;
      const expectedLink = `/workflows/${id}`;

      viewModel.attr('instance', {workflow: {id}});

      expect(viewModel.attr('workflowLink')).toBe(expectedLink);
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
});
