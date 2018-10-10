/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import * as aclUtils from '../utils/acl-utils';
import {
  getMappableTypes,
  isMappableType,
  getAssigneeType,
  allowedToMap,
} from '../ggrc_utils';
import Mappings from '../../models/mappers/mappings';
import Permission from '../../permission';
import TreeViewConfig from '../../apps/base_widgets';

'use strict';

describe('getMappableTypes() method', function () {
  beforeAll(function () {
    let canonicalMappings = {};
    let OBJECT_TYPES = [
      'DataAsset', 'Facility', 'Market', 'OrgGroup', 'Vendor', 'Process',
      'Product', 'Project', 'System', 'Regulation', 'Policy', 'Contract',
      'Standard', 'Program', 'Issue', 'Control', 'Requirement',
      'Objective', 'Audit', 'Assessment', 'AccessGroup',
      'Document', 'Risk', 'Threat',
    ];
    OBJECT_TYPES.forEach(function (item) {
      canonicalMappings[item] = {};
    });
    spyOn(Mappings, 'get_canonical_mappings_for')
      .and.returnValue(canonicalMappings);
  });

  it('always returns whitelisted items', function () {
    let whitelisted = ['Hello', 'World'];
    let result = getMappableTypes('AssessmentTemplate', {
      whitelist: whitelisted,
    });
    expect(_.intersection(result, whitelisted)).toEqual(whitelisted);
  });
  it('always remove forbidden items', function () {
    let forbidden = ['Policy', 'Process', 'Product', 'Program'];
    let list = getMappableTypes('DataAsset');
    let result = getMappableTypes('DataAsset', {
      forbidden: forbidden,
    });
    expect(_.difference(list, result).sort()).toEqual(forbidden.sort());
  });
  it('always leave whitelisted and remove forbidden items', function () {
    let forbidden = ['Policy', 'Process', 'Product', 'Program'];
    let whitelisted = ['Hello', 'World'];
    let list = getMappableTypes('DataAsset');
    let result = getMappableTypes('DataAsset', {
      forbidden: forbidden,
      whitelist: whitelisted,
    });
    let input = _.difference(list, result).concat(_.difference(result, list));
    let output = forbidden.concat(whitelisted);

    expect(input.sort()).toEqual(output.sort());
  });
});

describe('isMappableType() method', function () {
  it('returns false for AssessmentTemplate and  any type', function () {
    let result = isMappableType('AssessmentTemplate', 'Program');
    expect(result).toBe(false);
  });
  it('returns true for Program and Control', function () {
    let result = isMappableType('Program', 'Control');
    expect(result).toBe(true);
  });
});

describe('allowedToMap() method', () => {
  let baseWidgets;

  beforeAll(() => {
    baseWidgets = TreeViewConfig.attr('base_widgets_by_type');
    TreeViewConfig.attr('base_widgets_by_type', {
      Type1: ['Type2'],
    });
  });

  afterAll(() => {
    TreeViewConfig.attr('base_widgets_by_type', baseWidgets);
  });

  it('checks mapping rules', () => {
    spyOn(Permission, 'is_allowed_for');
    spyOn(Mappings, 'get_canonical_mappings_for');
    let result = allowedToMap('Issue', 'Audit', {isIssueUnmap: false});
    expect(result).toBeFalsy();
    expect(Mappings.get_canonical_mappings_for).not.toHaveBeenCalled();
    expect(Permission.is_allowed_for).not.toHaveBeenCalled();
  });

  it('checks mappable types when there is no additional mapping rules', () => {
    spyOn(Permission, 'is_allowed_for');
    spyOn(Mappings, 'get_canonical_mappings_for');
    let result = allowedToMap('Type1', 'Type2');
    expect(result).toBeFalsy();
    expect(Mappings.get_canonical_mappings_for).toHaveBeenCalledWith('Type1');
    expect(Permission.is_allowed_for).not.toHaveBeenCalled();
  });

  it('checks permissions to update source', () => {
    spyOn(Permission, 'is_allowed_for').and.returnValue(true);
    spyOn(Mappings, 'get_canonical_mappings_for')
      .and.returnValue({Type2: true});
    let result = allowedToMap('Type1', 'Type2');
    expect(result).toBeTruthy();
    expect(Mappings.get_canonical_mappings_for).toHaveBeenCalledWith('Type1');
    expect(Permission.is_allowed_for).toHaveBeenCalledWith('update', 'Type1');
    expect(Permission.is_allowed_for.calls.count()).toEqual(1);
  });

  it('checks permissions to update target', () => {
    spyOn(Permission, 'is_allowed_for').and.returnValue(true);
    spyOn(Mappings, 'get_canonical_mappings_for')
      .and.returnValue({Type2: true});
    let source = new can.Map({type: 'Type1'});
    let target = new can.Map({type: 'Type2'});
    let result = allowedToMap(source, target);
    expect(result).toBeTruthy();
    expect(Mappings.get_canonical_mappings_for).toHaveBeenCalledWith('Type1');
    expect(Permission.is_allowed_for.calls.count()).toEqual(2);
    expect(Permission.is_allowed_for.calls.argsFor(0))
      .toEqual(['update', source]);
    expect(Permission.is_allowed_for.calls.argsFor(1))
      .toEqual(['update', target]);
  });
});

describe('getAssigneeType() method', function () {
  let instance;

  beforeAll(function () {
    instance = {
      type: 'Assessment',
      id: 2147483647,
      access_control_list: [],
    };

    spyOn(aclUtils, 'getRolesForType').and.returnValue([
      {
        id: 1, object_type: 'Assessment', name: 'Admin',
      },
      {
        id: 3, object_type: 'Assessment', name: 'Verifiers',
      },
      {
        id: 4, object_type: 'Assessment', name: 'Creators',
      },
      {
        id: 5, object_type: 'Assessment', name: 'Assignees',
      },
    ]);
  });

  it('should return null. Empty ACL', function () {
    let userType = getAssigneeType(instance);
    expect(userType).toBeNull();
  });

  it('should return null. User is not in role', function () {
    let userType;
    instance.access_control_list = [
      {ac_role_id: 3, person: {id: 4}},
      {ac_role_id: 1, person: {id: 5}},
    ];

    userType = getAssigneeType(instance);
    expect(userType).toBeNull();
  });

  it('should return Verifiers type', function () {
    let userType;
    instance.access_control_list = [
      {ac_role_id: 3, person: {id: 1}},
      {ac_role_id: 1, person: {id: 3}},
    ];

    userType = getAssigneeType(instance);
    expect(userType).toEqual('Verifiers');
  });

  it('should return Verifiers and Creators types', function () {
    let userType;
    instance.access_control_list = [
      {ac_role_id: 3, person: {id: 1}},
      {ac_role_id: 1, person: {id: 3}},
      {ac_role_id: 4, person: {id: 1}},
      {ac_role_id: 3, person: {id: 5}},
    ];

    userType = getAssigneeType(instance);
    expect(userType.indexOf('Verifiers') > -1).toBeTruthy();
    expect(userType.indexOf('Creators') > -1).toBeTruthy();
  });

  it('should return Verifiers and Creators and Assigness types', function () {
    let userType;
    instance.access_control_list = [
      {ac_role_id: 3, person: {id: 1}},
      {ac_role_id: 1, person: {id: 3}},
      {ac_role_id: 4, person: {id: 1}},
      {ac_role_id: 3, person: {id: 5}},
      {ac_role_id: 5, person: {id: 1}},
    ];

    userType = getAssigneeType(instance);
    expect(userType.indexOf('Verifiers') > -1).toBeTruthy();
    expect(userType.indexOf('Creators') > -1).toBeTruthy();
    expect(userType.indexOf('Assignees') > -1).toBeTruthy();
  });

  it('should return string with types separated by commas', function () {
    let userType;
    let expectedString = 'Verifiers,Creators,Assignees';
    instance.access_control_list = [
      {ac_role_id: 3, person: {id: 1}},
      {ac_role_id: 1, person: {id: 3}},
      {ac_role_id: 4, person: {id: 1}},
      {ac_role_id: 3, person: {id: 5}},
      {ac_role_id: 5, person: {id: 1}},
    ];

    userType = getAssigneeType(instance);
    expect(userType).toEqual(expectedString);
  });
});
