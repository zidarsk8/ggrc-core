/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {
  makeFakeInstance,
  getComponentVM,
} from '../../../../js_specs/spec_helpers';
import * as aclUtils from '../../../plugins/utils/acl-utils';
import Component from '../access-control-list-roles-helper';
import Assessment from '../../../models/business-models/assessment';
import Control from '../../../models/business-models/control';


describe('access-control-list-roles-helper component', function () {
  'use strict';

  let viewModel;

  beforeEach(function () {
    viewModel = getComponentVM(Component);
  });

  describe('"setAutoPopulatedRoles" method', function () {
    let instance;

    it('should set current user for 2 roles', function () {
      spyOn(aclUtils, 'getRolesForType').and.returnValue([
        {
          object_type: 'Assessment',
          id: 5,
          name: 'Admin',
          default_to_current_user: true,
        },
        {
          object_type: 'Assessment',
          id: 7,
          name: 'SuperAdmin',
          default_to_current_user: true,
        },
        {
          object_type: 'Assessment',
          id: 8,
          name: 'Primary contacts',
          default_to_current_user: false,
        },
      ]);

      instance = makeFakeInstance({model: Assessment})({id: 25});
      viewModel.attr('instance', instance);
      expect(instance.access_control_list.length).toEqual(0);
      viewModel.setAutoPopulatedRoles();
      expect(instance.access_control_list.length).toEqual(2);
      expect(instance.access_control_list[0].ac_role_id)
        .toEqual(5);
      expect(instance.access_control_list[1].ac_role_id)
        .toEqual(7);
      expect(instance.access_control_list[0].person.id)
        .toEqual(1);
    });

    it('should set current user for 1 role', function () {
      spyOn(aclUtils, 'getRolesForType').and.returnValue([
        {
          object_type: 'Control',
          id: 6,
          name: 'Primary Contact',
          default_to_current_user: true,
        },
      ]);

      instance = makeFakeInstance({model: Control})({id: 25});
      viewModel.attr('instance', instance);
      expect(instance.access_control_list.length).toEqual(0);
      viewModel.setAutoPopulatedRoles();
      expect(instance.access_control_list.length).toEqual(1);
      expect(instance.access_control_list[0].ac_role_id)
        .toEqual(6);
      expect(instance.access_control_list[0].person.id)
        .toEqual(1);
    });
  });
});
