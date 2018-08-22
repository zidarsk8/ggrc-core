/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../tree-item-actions';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Permission from '../../../permission';
import * as SnapshotUtils from '../../../plugins/utils/snapshot-utils';

describe('tree-item-actions component', function () {
  let viewModel;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
    viewModel.attr('instance', new can.Map());
  });

  describe('isAllowedToMap get() method', () => {
    beforeEach(() => {
      spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
    });
    describe('returns false', () => {
      describe('if instance type is Assessment', ()=> {
        beforeEach(()=> {
          viewModel.attr('instance', {
            type: 'Assessment',
          });
        });

        it('and there is no audit', () => {
          viewModel.attr('instance.audit', null);

          let result = viewModel.attr('isAllowedToMap');

          expect(result).toBe(false);
        });

        it('and there is audit but it is not allowed to read audit', () => {
          viewModel.attr('instance.audit', {});
          spyOn(Permission, 'is_allowed_for').and.returnValue(false);

          let result = viewModel.attr('isAllowedToMap');

          expect(result).toBe(false);
        });
      });

      it('if instance type is in forbiddenMapList', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(true);
        viewModel.attr('instance.type', 'Workflow');

        let result = viewModel.attr('isAllowedToMap');

        expect(result).toBe(false);
      });

      it('if user has no rights to update instance', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(false);
        let result = viewModel.attr('isAllowedToMap');

        expect(result).toBe(false);
      });
    });

    describe('returns true', () => {
      describe('if instance type is Assessment', ()=> {
        beforeEach(()=> {
          viewModel.attr('instance', {
            type: 'Assessment',
          });
        });

        it('there is audit and it is allowed to read audit', () => {
          viewModel.attr('instance.audit', {});
          spyOn(Permission, 'is_allowed_for').and.returnValue(true);

          let result = viewModel.attr('isAllowedToMap');

          expect(result).toBe(true);
        });
      });

      it('if instance type is not in forbiddenMapList and ' +
        'has permissions to update instance', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(true);
        viewModel.attr('instance.type', 'Type');

        let result = viewModel.attr('isAllowedToMap');

        expect(result).toBe(true);
      });
    });
  });

  describe('isAllowedToEdit get() method', () => {
    describe('returns false', () => {
      it('if instance is archived', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(true);
        spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
        viewModel.attr('instance.type', 'Type');
        viewModel.attr('instance.archived', true);

        let result = viewModel.attr('isAllowedToEdit');
        expect(result).toBe(false);
      });

      it('if instance is snapshot', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(true);
        spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(true);
        viewModel.attr('instance.type', 'Type');
        viewModel.attr('instance.archived', false);

        let result = viewModel.attr('isAllowedToEdit');
        expect(result).toBe(false);
      });

      it('if instance type is in forbiddenEditList', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(true);
        spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
        viewModel.attr('instance.type', 'Cycle');
        viewModel.attr('instance.archived', false);

        let result = viewModel.attr('isAllowedToEdit');
        expect(result).toBe(false);
      });

      it('if user has not permissions to update instance', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(false);
        spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
        viewModel.attr('instance.type', 'Type');
        viewModel.attr('instance.archived', false);

        let result = viewModel.attr('isAllowedToEdit');
        expect(result).toBe(false);
      });
    });

    describe('returns true', () => {
      it('if allowed to edit instance', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(true);
        spyOn(SnapshotUtils, 'isSnapshot').and.returnValue(false);
        viewModel.attr('instance.type', 'Type');
        viewModel.attr('instance.archived', false);

        let result = viewModel.attr('isAllowedToEdit');
        expect(result).toBe(true);
      });
    });
  });
});
