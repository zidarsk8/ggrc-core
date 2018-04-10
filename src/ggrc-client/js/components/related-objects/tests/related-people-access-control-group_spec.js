/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as SnapshotUtils from '../../../plugins/utils/snapshot-utils';
import Component from '../related-people-access-control-group';
import Permission from '../../../permission';

describe('GGRC.Components.relatedPeopleAccessControlGroup', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = new (can.Map.extend(Component.prototype.viewModel));
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
});
