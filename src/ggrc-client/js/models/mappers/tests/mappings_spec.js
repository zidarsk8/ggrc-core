/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import * as Mappings from '../mappings';
import Permission from '../../../permission';

describe('Mappings', () => {
  let allTypes = [];
  let notMappableModels = [];
  let modules = {
    core: {
      models: [
        'AccessGroup',
        'AccountBalance',
        'Assessment',
        'AssessmentTemplate',
        'Audit',
        'Contract',
        'Control',
        'DataAsset',
        'Document',
        'Evidence',
        'Facility',
        'Issue',
        'KeyReport',
        'Market',
        'Metric',
        'Objective',
        'OrgGroup',
        'Person',
        'Policy',
        'Process',
        'Product',
        'ProductGroup',
        'Program',
        'Project',
        'Regulation',
        'Requirement',
        'Standard',
        'System',
        'Vendor',
        'Risk',
        'TechnologyEnvironment',
        'Threat',
      ],
      notMappable: ['Assessment', 'AssessmentTemplate', 'Evidence', 'Person'],
    },
    workflows: {
      models: [
        'TaskGroup',
        'TaskGroupTask',
        'Workflow',
        'CycleTaskGroupObjectTask',
        'CycleTaskGroup',
      ],
      notMappable: [
        'Workflow',
        'TaskGroup',
        'TaskGroupTask',
        'CycleTaskGroupObjectTask',
        'CycleTaskGroup',
      ],
    },
  };

  Object.keys(modules).forEach((module) => {
    allTypes = allTypes.concat(modules[module].models);
    notMappableModels = notMappableModels.concat(modules[module].notMappable);
  });

  const filtered = _.difference(allTypes, notMappableModels);

  const mappingRules = Object.freeze({
    AccessGroup: _.difference(filtered, ['AccessGroup']),
    AccountBalance: filtered,
    Assessment: _.difference(filtered, ['Audit', 'Person', 'Program', 'Project',
      'Workflow', 'Assessment', 'Document']),
    AssessmentTemplate: [],
    Audit: _.difference(filtered, ['Audit', 'Person', 'Program', 'Project',
      'Workflow', 'Assessment', 'Document']),
    Contract: _.difference(filtered, ['Contract']),
    Control: filtered,
    CycleTaskGroupObjectTask: _.difference(filtered, ['Person',
      'Workflow', 'Assessment', 'Document']),
    DataAsset: filtered,
    Evidence: [],
    Document: _.difference(filtered,
      ['Audit', 'Assessment', 'Document', 'Person', 'Workflow']),
    Facility: filtered,
    Issue: _.difference(filtered, [
      'Audit', 'Person', 'Workflow', 'Assessment']),
    KeyReport: filtered,
    Market: filtered,
    Metric: filtered,
    Objective: filtered,
    OrgGroup: filtered,
    Person: [],
    Policy: _.difference(filtered, ['Policy']),
    Process: filtered,
    Product: filtered,
    ProductGroup: filtered,
    Program: _.difference(allTypes,
      ['Audit', 'Assessment', 'Person']
        .concat(modules.core.notMappable, modules.workflows.notMappable)),
    Project: filtered,
    Regulation: _.difference(filtered, ['Regulation']),
    Risk: filtered,
    Requirement: filtered,
    Standard: _.difference(filtered, ['Standard']),
    System: filtered,
    TaskGroup: _.difference(filtered, ['Audit', 'Person',
      'Workflow', 'Assessment', 'Document']),
    TechnologyEnvironment: filtered,
    Threat: filtered,
    Vendor: filtered,
    MultitypeSearch: _.difference(allTypes, ['CycleTaskGroup']),
  });

  describe('getMappingList() method', () => {
    let types = allTypes.concat('MultitypeSearch');
    let modelsForTests = _.difference(types, [
      'TaskGroupTask',
      'CycleTaskGroup',
      'Workflow',
    ]);

    modelsForTests.forEach(function (type) {
      it('returns mappable types for ' + type, function () {
        let expectedModels = mappingRules[type];
        let result = Mappings.getMappingList(type);

        expect(expectedModels.sort()).toEqual(result.sort());
      });
    });
  });

  describe('allowedToMap() method', () => {
    beforeEach(() => {
      spyOn(Permission, 'is_allowed_for').and.returnValue(true);
    });

    it('checks that types are mappable', () => {
      let result = Mappings.allowedToMap('SourceType', 'TargetType');

      expect(result).toBeFalsy();
      expect(Permission.is_allowed_for).not.toHaveBeenCalled();
    });

    it('checks map collection', () => {
      let result = Mappings.allowedToMap('Program', 'Document');
      expect(result).toBeTruthy();
    });

    it('checks externalMap collection', () => {
      let result = Mappings.allowedToMap('Control', 'Risk');
      expect(result).toBeTruthy();
    });

    it('checks permissions to update source', () => {
      let result = Mappings.allowedToMap('Program', 'Document');

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for)
        .toHaveBeenCalledWith('update', 'Program');
      expect(Permission.is_allowed_for.calls.count()).toEqual(1);
    });

    it('checks permissions to update target', () => {
      let source = new CanMap({type: 'Program'});
      let target = new CanMap({type: 'Document'});
      let result = Mappings.allowedToMap(source, target);

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for.calls.count()).toEqual(2);
      expect(Permission.is_allowed_for.calls.argsFor(0))
        .toEqual(['update', source]);
      expect(Permission.is_allowed_for.calls.argsFor(1))
        .toEqual(['update', target]);
    });
  });

  describe('allowedToCreate() method', () => {
    beforeEach(() => {
      spyOn(Permission, 'is_allowed_for').and.returnValue(true);
    });

    it('checks that types are mappable', () => {
      let result = Mappings.allowedToCreate('SourceType', 'TargetType');

      expect(result).toBeFalsy();
      expect(Permission.is_allowed_for).not.toHaveBeenCalled();
    });

    it('checks permissions to update source', () => {
      let result = Mappings.allowedToCreate('Program', 'Audit');

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for)
        .toHaveBeenCalledWith('update', 'Program');
      expect(Permission.is_allowed_for.calls.count()).toEqual(1);
    });

    it('checks permissions to update target', () => {
      let source = new CanMap({type: 'Program'});
      let target = new CanMap({type: 'Audit'});
      let result = Mappings.allowedToCreate(source, target);

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for.calls.count()).toEqual(2);
      expect(Permission.is_allowed_for.calls.argsFor(0))
        .toEqual(['update', source]);
      expect(Permission.is_allowed_for.calls.argsFor(1))
        .toEqual(['update', target]);
    });
  });

  describe('allowedToUnmap() method', () => {
    beforeEach(() => {
      spyOn(Permission, 'is_allowed_for').and.returnValue(true);
    });

    it('checks that types are unmappable', () => {
      let result = Mappings.allowedToUnmap('SourceType', 'TargetType');

      expect(result).toBeFalsy();
      expect(Permission.is_allowed_for).not.toHaveBeenCalled();
    });

    it('checks permissions to update source', () => {
      let result = Mappings.allowedToUnmap('Program', 'Document');

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for)
        .toHaveBeenCalledWith('update', 'Program');
      expect(Permission.is_allowed_for.calls.count()).toEqual(1);
    });

    it('checks permissions to update target', () => {
      let source = new CanMap({type: 'Program'});
      let target = new CanMap({type: 'Document'});
      let result = Mappings.allowedToUnmap(source, target);

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for.calls.count()).toEqual(2);
      expect(Permission.is_allowed_for.calls.argsFor(0))
        .toEqual(['update', source]);
      expect(Permission.is_allowed_for.calls.argsFor(1))
        .toEqual(['update', target]);
    });
  });
});
