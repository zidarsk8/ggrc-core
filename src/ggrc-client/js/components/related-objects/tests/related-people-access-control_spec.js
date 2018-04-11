/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import Component from '../related-people-access-control';
import * as aclUtils from '../../../plugins/utils/acl-utils';

describe('GGRC.relatedPeopleAccessControl', function () {
  let viewModel;

  beforeAll(function () {
    viewModel = new (can.Map.extend(Component.prototype.viewModel));
  });

  describe('"updateRoles" method', () => {
    let args;

    beforeEach(() => {
      args = {};
      spyOn(viewModel, 'performUpdate');
      spyOn(viewModel, 'dispatch');
    });

    it('calls "performUpdate" method', () => {
      viewModel.updateRoles(args);

      expect(viewModel.performUpdate).toHaveBeenCalledWith(args);
    });

    it('dispatches "saveCustomRole" event with groupId', () => {
      args.roleId = 711;
      viewModel.updateRoles(args);

      expect(viewModel.dispatch).toHaveBeenCalledWith({
        type: 'saveCustomRole',
        groupId: args.roleId,
      });
    });

    it('pushes action into deferredSave if it is defined', () => {
      viewModel.attr('deferredSave', {
        push: jasmine.createSpy(),
      });

      viewModel.updateRoles(args);
      expect(viewModel.performUpdate.calls.count()).toBe(1);

      viewModel.attr('deferredSave').push.calls.allArgs()[0][0]();
      expect(viewModel.performUpdate.calls.count()).toBe(2);
    });
  });

  describe('"performUpdate" method', () => {
    beforeEach(() => {
      spyOn(viewModel, 'updateAccessContolList');
      spyOn(viewModel, 'checkConflicts');
    });

    it('calls "updateAccessContolList" method', () => {
      const args = {
        people: 'mockPeople',
        roleId: 'mockRoleId',
      };

      viewModel.performUpdate(args);

      expect(viewModel.updateAccessContolList)
        .toHaveBeenCalledWith(args.people, args.roleId);
    });

    it('calls "checkConflicts" method if conflictRoles is not empty', () => {
      const args = {
        roleTitle: 'mockRoleTitle',
      };
      viewModel.attr('conflictRoles', [1, 2]);

      viewModel.performUpdate(args);

      expect(viewModel.checkConflicts).toHaveBeenCalledWith(args.roleTitle);
    });

    it('does not call "checkConflicts" method if conflictRoles is empty',
      () => {
        viewModel.attr('conflictRoles', []);

        viewModel.performUpdate({});

        expect(viewModel.checkConflicts).not.toHaveBeenCalled();
      });
  });

  beforeEach(() => {
    spyOn(aclUtils, 'getRolesForType').and.returnValue([
      {id: 1, name: 'Admin', object_type: 'Control'},
      {id: 3, name: 'Primary Contacts', object_type: 'Control'},
      {id: 4, name: 'Secondary Contacts', object_type: 'Control'},
      {id: 5, name: 'Principal Assignees', object_type: 'Control'},
      {id: 6, name: 'Secondary Assignees', object_type: 'Control'},
    ]);
  });

  describe('"getFilteredRoles" method', function () {
    let instance;
    let getFilteredRolesMethod;

    beforeAll(function () {
      instance = {
        'class': {
          model_singular: 'Control',
        },
      };
    });

    beforeEach(function () {
      viewModel.attr('instance', instance);
      viewModel.attr('includeRoles', []);
      viewModel.attr('excludeRoles', []);

      getFilteredRolesMethod = viewModel.getFilteredRoles.bind(viewModel);
    });

    it('should return all roles related to instance type', function () {
      let roles = getFilteredRolesMethod();
      expect(roles.length).toBe(5);
    });

    it('should return roles from IncludeRoles list', function () {
      let roles;
      let include = ['Admin', 'Secondary Contacts', 'Principal Assignees'];

      viewModel.attr('includeRoles', include);
      roles = getFilteredRolesMethod();

      expect(roles.length).toBe(3);
      expect(roles[2].name).toEqual('Principal Assignees');
    });

    it('should return all roles except roles from ExcludeRoles list',
      function () {
        let roles;
        let exclude = ['Admin', 'Secondary Contacts', 'Principal Assignees'];

        viewModel.attr('excludeRoles', exclude);
        roles = getFilteredRolesMethod();

        expect(roles.length).toBe(2);
        expect(roles[1].name).toEqual('Secondary Assignees');
      }
    );

    it('should return roles from IncludeRoles withou roles from ExcludeRoles',
      function () {
        let roles;
        let include = ['Admin', 'Secondary Contacts', 'Principal Assignees'];
        let exclude = ['Admin', 'Principal Assignees', 'Primary Contacts'];

        viewModel.attr('includeRoles', include);
        viewModel.attr('excludeRoles', exclude);
        roles = getFilteredRolesMethod();

        expect(roles.length).toBe(1);
        expect(roles[0].name).toEqual('Secondary Contacts');
      }
    );
  });

  describe('"checkConflicts" method', function () {
    let instance;

    beforeAll(function () {
      instance = new can.Map({
        'class': {
          model_singular: 'Control',
        },
      });
    });

    beforeEach(function () {
      viewModel.attr('instance', instance);
      viewModel.attr('includeRoles', []);
      viewModel.attr('excludeRoles', []);
    });

    function isGroupsHasConflict(conflictRoles, acl) {
      let groups;
      instance.attr('access_control_list', acl);
      viewModel.attr('instance', instance);
      viewModel.attr('groups', viewModel.getRoleList());
      groups = viewModel.attr('groups');

      return viewModel
        .isGroupsHasConflict(groups, conflictRoles);
    }

    function isCurrentGroupHasConflict(currentGroup, conflictRoles, acl) {
      let groups;
      instance.attr('access_control_list', acl);
      viewModel.attr('instance', instance);
      viewModel.attr('groups', viewModel.getRoleList());
      groups = viewModel.attr('groups');

      return viewModel
        .isCurrentGroupHasConflict(currentGroup, groups, conflictRoles);
    }

    it('"isGroupsHasConflict" should return TRUE. 2 groups conflict',
      function () {
        let conflictRoles = ['Admin', 'Primary Contacts'];
        let hasConflicts = false;
        let acl = [
          {ac_role_id: 1, person: {id: 1}},
          {ac_role_id: 1, person: {id: 2}},
          {ac_role_id: 1, person: {id: 3}},
          // conflict with ac_role_id: 1
          {ac_role_id: 3, person: {id: 3}},
          {ac_role_id: 3, person: {id: 4}},
          {ac_role_id: 4, person: {id: 1}},
        ];

        hasConflicts = isGroupsHasConflict(conflictRoles, acl);
        expect(hasConflicts).toBeTruthy();
      }
    );

    it('"isGroupsHasConflict" should return TRUE. 3 groups conflict',
      function () {
        let conflictRoles = [
          'Admin',
          'Primary Contacts',
          'Secondary Assignees',
        ];
        let hasConflicts = false;
        let acl = [
          {ac_role_id: 1, person: {id: 1}},
          {ac_role_id: 1, person: {id: 2}},
          {ac_role_id: 1, person: {id: 3}},

          // conflict with ac_role_id: 1
          {ac_role_id: 3, person: {id: 3}},
          {ac_role_id: 3, person: {id: 4}},
          {ac_role_id: 4, person: {id: 1}},

          // conflict with ac_role_id 3
          {ac_role_id: 6, person: {id: 4}},
        ];

        hasConflicts = isGroupsHasConflict(conflictRoles, acl);
        expect(hasConflicts).toBeTruthy();
      }
    );

    it('"isGroupsHasConflict" should return FALSE. 3 groups conflict',
      function () {
        let conflictRoles = [
          'Admin',
          'Primary Contacts',
          'Secondary Assignees',
        ];
        let hasConflicts = false;
        let acl = [
          {ac_role_id: 1, person: {id: 1}},
          {ac_role_id: 1, person: {id: 2}},
          {ac_role_id: 1, person: {id: 3}},
          {ac_role_id: 3, person: {id: 7}},
          {ac_role_id: 3, person: {id: 4}},
          {ac_role_id: 4, person: {id: 1}},
          {ac_role_id: 6, person: {id: 14}},
        ];

        hasConflicts = isGroupsHasConflict(conflictRoles, acl);

        expect(hasConflicts).toBeFalsy();
      }
    );

    it('"isCurrentGroupHasConflict" should return TRUE. 2 groups conflict',
      function () {
        let conflictRoles = ['Admin', 'Primary Contacts'];
        let hasConflicts = false;
        let acl = [
          {ac_role_id: 1, person: {id: 1}},
          {ac_role_id: 1, person: {id: 2}},
          {ac_role_id: 1, person: {id: 3}},
          // conflict with ac_role_id: 1
          {ac_role_id: 3, person: {id: 3}},
          {ac_role_id: 3, person: {id: 4}},
          {ac_role_id: 4, person: {id: 1}},
        ];

        hasConflicts = isCurrentGroupHasConflict('Admin', conflictRoles, acl);
        expect(hasConflicts).toBeTruthy();
      }
    );

    it('"isCurrentGroupHasConflict" should return TRUE. 3 groups conflict',
      function () {
        let conflictRoles = [
          'Admin',
          'Primary Contacts',
          'Secondary Assignees',
        ];
        let hasConflicts = false;
        let acl = [
          {ac_role_id: 1, person: {id: 1}},
          {ac_role_id: 1, person: {id: 2}},
          {ac_role_id: 1, person: {id: 3}},

          // conflict with ac_role_id: 1
          {ac_role_id: 3, person: {id: 3}},
          {ac_role_id: 3, person: {id: 4}},
          {ac_role_id: 4, person: {id: 1}},

          // conflict with ac_role_id 3
          {ac_role_id: 6, person: {id: 4}},
        ];

        hasConflicts = isCurrentGroupHasConflict('Admin', conflictRoles, acl);
        expect(hasConflicts).toBeTruthy();
      }
    );

    it('"isCurrentGroupHasConflict" should return FALSE. 3 groups conflict',
      function () {
        let conflictRoles = [
          'Admin',
          'Primary Contacts',
          'Secondary Assignees',
        ];
        let hasConflicts = false;
        let acl = [
          {ac_role_id: 1, person: {id: 1}},
          {ac_role_id: 1, person: {id: 2}},
          {ac_role_id: 1, person: {id: 3}},
          {ac_role_id: 3, person: {id: 7}},
          {ac_role_id: 3, person: {id: 4}},
          {ac_role_id: 4, person: {id: 1}},
          {ac_role_id: 6, person: {id: 14}},
        ];

        hasConflicts = isCurrentGroupHasConflict('Admin', conflictRoles, acl);
        expect(hasConflicts).toBeFalsy();
      }
    );
  });

  describe('"setGroupOrder" method', function () {
    const groups = [
      {title: 'Primary Contacts', id: 1},
      {title: 'Secondary Contacts', id: 2},
      {title: 'Verifier', id: 3},
      {title: 'Admin', id: 4},
      {title: 'Creator', id: 5},
      {title: 'Assessor', id: 6},
    ];

    function checkOrder(orderArray) {
      let result = viewModel.setGroupOrder(groups, orderArray);

      expect(result.length).toBe(6);
      expect(result[0].title).toEqual('Primary Contacts');
      expect(result[2].title).toEqual('Verifier');
      expect(result[5].title).toEqual('Assessor');
    }

    it('should not change order of groups. Empty order array', function () {
      checkOrder([]);
    });

    it('should not change order of groups. Without order array', function () {
      checkOrder();
    });

    it('should not change order of groups. Order array has wrong titles',
      function () {
        let orderArray = ['My Role', 'Primary', 'Contacts'];
        checkOrder(orderArray);
      }
    );

    it('should change order of groups', function () {
      let orderArray = ['Creator', 'Assessor', 'Verifier'];
      let result = viewModel.setGroupOrder(groups, orderArray);

      expect(result.length).toBe(6);
      expect(result[0].title).toEqual('Creator');
      expect(result[1].title).toEqual('Assessor');
      expect(result[2].title).toEqual('Verifier');
    });
  });
});
