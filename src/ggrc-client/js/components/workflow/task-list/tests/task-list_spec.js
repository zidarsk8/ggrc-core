/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../task-list';
import {getComponentVM} from '../../../../../js_specs/spec_helpers';
import Permission from '../../../../permission';

describe('task-list component', () => {
  let viewModel;

  beforeEach(function () {
    viewModel = getComponentVM(Component);
  });

  describe('showCreateTaskButton attribute', () => {
    describe('get() method', () => {
      beforeEach(function () {
        viewModel.attr('baseInstance', {});
      });

      describe('returns false', () => {
        it('when there are no "update" permissions for the passed task group',
          function () {
            spyOn(Permission, 'is_allowed_for').and.returnValue(false);
            const result = viewModel.attr('showCreateTaskButton');
            expect(result).toBe(false);
            expect(Permission.is_allowed_for).toHaveBeenCalledWith(
              'update',
              viewModel.attr('baseInstance')
            );
          });

        it('when appropriate workflow is inactive', function () {
          viewModel.attr('workflow', {status: false});
          expect(viewModel.attr('showCreateTaskButton')).toBe(false);
        });
      });
    });
  });

  describe('updatePagingAfterCreate()', () => {
    beforeEach(function () {
      viewModel.attr('baseInstance', {});
      viewModel.attr('paging.count', 100);
    });

    describe('when page is not first', () => {
      beforeEach(function () {
        viewModel.attr('paging.current', 3);
      });

      it('sets first page for pagination', function () {
        viewModel.updatePagingAfterCreate();
        expect(viewModel.attr('paging.current')).toBe(1);
      });
    });

    describe('when page is first', () => {
      beforeEach(function () {
        viewModel.attr('paging.current', 1);
      });

      it('dispatches "refreshInstance" event for base instance',
        function () {
          const dispatch = spyOn(viewModel.baseInstance, 'dispatch');
          viewModel.updatePagingAfterCreate();
          expect(dispatch).toHaveBeenCalledWith('refreshInstance');
        });
    });
  });

  describe('events', () => {
    let events;

    beforeEach(function () {
      events = Component.prototype.events;
    });

    describe('"{CMS.Models.TaskGroupTask} created"() event', () => {
      let handler;
      let eventsScope;

      beforeEach(function () {
        eventsScope = {viewModel};
        handler = events['{CMS.Models.TaskGroupTask} created']
          .bind(eventsScope);
      });

      it('updates page items', function () {
        const update = spyOn(viewModel, 'updatePagingAfterCreate');
        handler();
        expect(update).toHaveBeenCalled();
      });
    });
  });
});
