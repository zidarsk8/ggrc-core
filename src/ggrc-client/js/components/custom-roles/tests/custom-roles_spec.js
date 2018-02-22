/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../custom-roles';
import {getComponentVM} from '../../../../js_specs/spec_helpers';

describe('custom-roles component', () => {
  let vm;

  beforeEach(() => {
    vm = getComponentVM(Component);
  });

  describe('isReadOnlyForInstance() method', () => {
    it('returns false if there is no instance', () => {
      let falseInstances = [null, undefined, '', 0, false, NaN];

      falseInstances.forEach((instance) => {
        expect(vm.isReadOnlyForInstance(instance)).toBe(false);
      });
    });

    it('returns value of instance.class.isProposable if instance is defined',
      () => {
        let instance = {
          'class': {
            isProposable: true,
          },
        };
        expect(vm.isReadOnlyForInstance(instance)).toBe(true);

        instance.class.isProposable = false;
        expect(vm.isReadOnlyForInstance(instance)).toBe(false);
      });
  });

  describe('filterACL() method', () => {
    let acl;

    beforeEach(() => {
      spyOn(vm, 'isReadOnlyForInstance');
      vm.attr('instance', {});
    });

    it('replaces access_control_list of instance ' +
    'excluding elements without id', () => {
      acl = [{id: 123}, {}, {id: 321}];

      vm.attr('instance.access_control_list', acl);
      vm.filterACL();

      expect(vm.attr('instance.access_control_list').serialize())
        .toEqual(acl.filter((role) => role.id));
    });
  });

  describe('save() method', () => {
    let args;
    let saveDfd;

    beforeEach(() => {
      args = {};
      spyOn(vm, 'isReadOnlyForInstance');
      saveDfd = new can.Deferred();
      vm.attr('instance', {
        save: jasmine.createSpy().and.returnValue(saveDfd),
      });
      spyOn(vm.attr('instance'), 'dispatch');
    });

    it('sets groupId of args to updatableGroupId attribute', () => {
      vm.attr('updatableGroupId', null);
      args.groupId = 123;
      vm.save(args);
      expect(vm.attr('updatableGroupId')).toBe(args.groupId);
    });

    describe('after getting response', () => {
      beforeEach(() => {
        saveDfd.resolve();
        spyOn(vm, 'filterACL');
      });

      it('calls filterACL', () => {
        vm.save(args);
        expect(vm.filterACL).toHaveBeenCalled();
      });

      it('dispatches refreshInstance event on instance', () => {
        vm.save(args);
        expect(vm.attr('instance').dispatch)
          .toHaveBeenCalledWith('refreshInstance');
      });

      it('sets null to updatableGroupId attribute', () => {
        vm.save(args);
        expect(vm.attr('updatableGroupId')).toBe(null);
      });
    });
  });
});
