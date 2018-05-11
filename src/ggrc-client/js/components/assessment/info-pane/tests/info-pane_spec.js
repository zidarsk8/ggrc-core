/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import tracker from '../../../../tracker';
import DeferredTransaction from '../../../../plugins/utils/deferred-transaction-utils';
import Permission from '../../../../permission';

describe('GGRC.Components.assessmentInfoPane', function () {
  let vm;
  let instanceSave;

  beforeEach(function () {
    instanceSave = can.Deferred();
    vm = GGRC.Components.getViewModel('assessmentInfoPane');
    vm.attr('instance', {
      save: () => instanceSave,
    });
  });

  describe('editMode attribute', function () {
    const editableStatuses = ['Not Started', 'In Progress', 'Rework Needed'];
    const nonEditableStates = ['In Review', 'Completed', 'Deprecated'];
    const allStatuses = editableStatuses.concat(nonEditableStates);

    describe('get() method', function () {
      it('returns false if instance is archived', function () {
        vm.attr('instance.archived', true);

        allStatuses.forEach((status) => {
          vm.attr('instance.status', status);
          expect(vm.attr('editMode')).toBe(false);
        });
      });

      describe('if instance is not archived', function () {
        it('returns true if instance status is editable otherwise false',
          function () {
            allStatuses.forEach((status) => {
              vm.attr('instance.status', status);
              expect(vm.attr('editMode'))
                .toBe(editableStatuses.includes(status));
            });
          });
      });
    });
  });

  describe('isAllowedToMap attribute', ()=> {
    describe('get() method', ()=> {
      it(`returns true if there is audit
        and it is allowed to read instance.audit`, ()=> {
          vm.attr('instance.audit', {});
          spyOn(Permission, 'is_allowed_for').and.returnValue(true);

          let result = vm.attr('isAllowedToMap');

          expect(result).toBe(true);
        });
      it('returns false if there is no audit', ()=> {
        vm.attr('instance.audit', null);

        let result = vm.attr('isAllowedToMap');

        expect(result).toBe(false);
      });

      it(`returns false if there is audit
        but it is not allowed to read instance.audit`, ()=> {
          vm.attr('instance.audit', {});
          spyOn(Permission, 'is_allowed_for').and.returnValue(false);

          let result = vm.attr('isAllowedToMap');

          expect(result).toBe(false);
        });
    });
  });

  describe('onStateChange() method', () => {
    let method;

    beforeEach(() => {
      method = vm.onStateChange.bind(vm);
      spyOn(tracker, 'start').and.returnValue(() => {});

      vm.attr('deferredSave', new DeferredTransaction((resolve, reject) => {
        vm.attr('instance').save().done(resolve).fail(reject);
      }, 0, true));
    });

    it('prevents state change to deprecated for archived instance', (done) => {
      vm.attr('instance.archived', true);
      vm.attr('instance.status', 'Completed');

      method({
        state: vm.attr('deprecatedState'),
      }).then(() => {
        expect(vm.attr('instance.status')).toBe('Completed');
        done();
      });
    });

    it('prevents state change to initial for archived instance', (done) => {
      vm.attr('instance.archived', true);
      vm.attr('instance.status', 'Completed');

      method({
        state: vm.attr('initialState'),
      }).then(() => {
        expect(vm.attr('instance.status')).toBe('Completed');
        done();
      });
    });

    it('returns status back on undo action', (done) => {
      vm.attr('instance.previousStatus', 'FooBar');
      instanceSave.resolve();

      method({
        undo: true,
        status: 'newStatus',
      }).then(() => {
        expect(vm.attr('instance.status')).toBe('FooBar');
        done();
      });
    });

    it('resets status after conflict', (done) => {
      vm.attr('instance.status', 'Baz');
      instanceSave.reject({}, {
        status: 409,
        remoteObject: {
          status: 'Foo',
        },
      });

      method({
        status: 'Bar',
      }).fail(() => {
        expect(vm.attr('instance.status')).toBe('Foo');
        done();
      });
    });
  });

  describe('saveGlobalAttributes() method', () => {
    let method;
    let event;

    beforeEach(() => {
      method = vm.saveGlobalAttributes.bind(vm);
      vm.attr('deferredSave', {
        push: jasmine.createSpy(),
      });
      vm.attr('instance', {
        customAttr: jasmine.createSpy(),
      });
    });

    it('pushes callback into deferredSave which calls customAttr method',
      () => {
        event = {
          globalAttributes: new can.Map({'1': true}),
        };

        method(event);

        let callback = vm.attr('deferredSave').push.calls.allArgs()[0][0];
        callback();
        expect(vm.attr('instance').customAttr).toHaveBeenCalledWith('1', true);
      });
  });
});
