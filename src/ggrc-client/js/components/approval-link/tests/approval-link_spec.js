/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../approval-link';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Permission from '../../../permission';
import * as aclUtils from '../../../plugins/utils/acl-utils';

describe('approval-link component', ()=> {
  let viewModel;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
  });

  describe('isReviewer get()', () => {
    let assigneeRole;

    beforeAll(() => {
      assigneeRole = {
        id: -1,
      };
      spyOn(aclUtils, 'getRole').and.returnValue(assigneeRole);
    });

    it('returns false when reviewTask is not set', () => {
      viewModel.attr('reviewTask', null);
      spyOn(Permission, 'is_allowed').and.returnValue(false);

      let result = viewModel.attr('isReviewer');

      expect(result).toBe(false);
    });

    it('returns true when user is Admin', () => {
      viewModel.attr('reviewTask', {});
      spyOn(Permission, 'is_allowed').and.returnValue(true);

      let result = viewModel.attr('isReviewer');

      expect(result).toBe(true);
    });

    it('returns false when ACL person does not match current user', () => {
      viewModel.attr('reviewTask', {
        access_control_list: {
          ac_role_id: assigneeRole.id,
          person: {
            id: 12345,
          },
        },
      });
      spyOn(Permission, 'is_allowed').and.returnValue(false);

      let result = viewModel.attr('isReviewer');

      expect(result).toBe(false);
    });

    it('returns false when ACL role non-Task Assignees for user', () => {
      viewModel.attr('reviewTask', {
        access_control_list: {
          ac_role_id: 12,
          person: {
            id: 12345,
          },
        },
      });
      spyOn(Permission, 'is_allowed').and.returnValue(false);

      let result = viewModel.attr('isReviewer');

      expect(result).toBe(false);
    });

    it('returns true when ACL person role matches current user', () => {
      viewModel.attr('reviewTask', {
        access_control_list: {
          ac_role_id: assigneeRole.id,
          person: {
            id: 1,
          },
        },
      });
      spyOn(Permission, 'is_allowed').and.returnValue(false);

      let result = viewModel.attr('isReviewer');

      expect(result).toBe(true);
    });
  });
});
