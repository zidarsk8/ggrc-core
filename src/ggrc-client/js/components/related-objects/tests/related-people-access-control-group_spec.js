/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as SnapshotUtils from '../../../plugins/utils/snapshot-utils';
import Permission from '../../../permission';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../related-people-access-control-group';

describe('related-people-access-control-group component', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
    viewModel.attr('instance', {});
  });

  describe('canEdit prop', () => {
    it('returns "false" when instance is snapshot', () => {
      spyOn(Permission, 'is_allowed_for').and.returnValue(true);
      viewModel.instance.attr('archived', false);
      viewModel.attr('updatableGroupId', null);
      viewModel.attr('isNewInstance', false);

      spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(true);

      expect(viewModel.attr('canEdit')).toEqual(false);
    });

    it('returns "false" when instance is archived', () => {
      spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
      spyOn(Permission, 'is_allowed_for').and.returnValue(true);
      viewModel.attr('updatableGroupId', null);
      viewModel.attr('isNewInstance', false);

      viewModel.instance.attr('archived', true);

      expect(viewModel.attr('canEdit')).toEqual(false);
    });

    it('returns "false" when there is updatableGroupId', () => {
      spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
      viewModel.instance.attr('archived', false);
      viewModel.attr('isNewInstance', false);
      spyOn(Permission, 'is_allowed_for').and.returnValue(true);

      viewModel.attr('updatableGroupId', 'groupId');

      expect(viewModel.attr('canEdit')).toEqual(false);
    });

    it('returns "false" when user has no update permissions', () => {
      spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
      viewModel.instance.attr('archived', false);
      viewModel.attr('updatableGroupId', null);
      viewModel.attr('isNewInstance', false);

      spyOn(Permission, 'is_allowed_for').and.returnValue(false);

      expect(viewModel.attr('canEdit')).toEqual(false);
    });

    it('returns "false" when is readonly', () => {
      spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
      spyOn(Permission, 'is_allowed_for').and.returnValue(false);
      viewModel.instance.attr('archived', false);
      viewModel.attr('updatableGroupId', null);
      viewModel.attr('isNewInstance', true);
      viewModel.attr('isReadonly', true);

      expect(viewModel.attr('canEdit')).toEqual(false);
    });

    it('returns "true" when new instance', () => {
      spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
      spyOn(Permission, 'is_allowed_for').and.returnValue(false);
      viewModel.instance.attr('archived', false);
      viewModel.attr('updatableGroupId', null);

      viewModel.attr('isNewInstance', true);

      expect(viewModel.attr('canEdit')).toEqual(true);
    });

    it('returns "true" when user has update permissions', () => {
      spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
      viewModel.instance.attr('archived', false);
      viewModel.attr('updatableGroupId', null);
      viewModel.attr('isNewInstance', false);

      spyOn(Permission, 'is_allowed_for').and.returnValue(true);

      expect(viewModel.attr('canEdit')).toEqual(true);
    });
  });

  describe('canAdd prop', () => {
    let people = ['user1'];

    it('returns "false" when singleUserRole is "true" and people.length > 0',
      () => {
        viewModel.attr('people', people);
        viewModel.attr('singleUserRole', true);

        let result = viewModel.attr('canAdd');

        expect(result).toEqual(false);
      });

    it('returns "true" when singleUserRole is "false" and people.length > 0',
      () => {
        viewModel.attr('people', people);
        viewModel.attr('singleUserRole', false);

        let result = viewModel.attr('canAdd');

        expect(result).toEqual(true);
      });

    it('returns "true" when singleUserRole is "false" and people.length is 0',
      () => {
        viewModel.attr('people', []);
        viewModel.attr('singleUserRole', false);

        let result = viewModel.attr('canAdd');

        expect(result).toEqual(true);
      });

    it('returns "true" when singleUserRole is "true" and people.length is 0',
      () => {
        viewModel.attr('people', []);
        viewModel.attr('singleUserRole', true);

        let result = viewModel.attr('canAdd');

        expect(result).toEqual(true);
      });
  });

  describe('check methods for updating "people" property', () => {
    let peopleList = [
      {id: 1, desc: 'Existent Person'},
      {id: 2, desc: 'Non-Existent Person'},
    ];

    beforeEach(() => {
      viewModel.attr('people', [peopleList[0]]);
      viewModel.attr('groupId', 1);
      viewModel.attr('title', peopleList[0].desc);
    });

    describe('"addPerson" method', () => {
      it('should add person to "people" list if not present', () => {
        viewModel.addPerson(peopleList[1], viewModel.attr('groupId'));
        expect(viewModel.attr('people').length).toBe(2);
      });

      it('should not add person to "people" list if present', () => {
        viewModel.addPerson(peopleList[0], viewModel.attr('groupId'));
        expect(viewModel.attr('people').length).toBe(1);
      });
    });

    describe('"removePerson" method', () => {
      it('should remove person from "people" list if present', () => {
        viewModel.removePerson({person: peopleList[0]});
        expect(viewModel.attr('people').length).toBe(0);
      });

      it('should not remove person from "people" list if not present', () => {
        let count = viewModel.attr('people').length;
        viewModel.removePerson({person: peopleList[1]});
        expect(viewModel.attr('people').length).toBe(count);
      });
    });
  });
});
