/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import * as Mappings from '../mappings';
import Permission from '../../../permission';

describe('Mappings', function () {
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
      scope: {
        notMappable: ['Audit'],
      },
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

  Object.keys(modules).forEach(function (module) {
    allTypes = allTypes.concat(modules[module].models);
    notMappableModels = notMappableModels.concat(modules[module].notMappable);
  });

  const filtered = _.difference(allTypes, notMappableModels);

  const unmappingRules = Object.freeze({
    AccessGroup: _.difference(filtered,
      modules.core.scope.notMappable, ['AccessGroup']),
    AccountBalance: _.difference(filtered, modules.core.scope.notMappable),
    Assessment: _.difference(filtered, ['Audit', 'Person', 'Program', 'Project',
      'Workflow', 'Assessment', 'Document']),
    AssessmentTemplate: [],
    Audit: ['Issue'],
    Contract: _.difference(filtered, ['Audit', 'Contract']),
    Control: _.difference(filtered, ['Audit']),
    CycleTaskGroupObjectTask: _.difference(filtered, ['Person',
      'Workflow', 'Assessment', 'Document']),
    DataAsset: _.difference(filtered, modules.core.scope.notMappable),
    Evidence: [],
    Document: _.difference(filtered,
      ['Audit', 'Assessment', 'Document', 'Person', 'Workflow']),
    Facility: _.difference(filtered, modules.core.scope.notMappable),
    Issue: _.difference(allTypes,
      ['Person', 'AssessmentTemplate', 'Evidence']
        .concat(modules.workflows.notMappable)),
    KeyReport: _.difference(filtered, modules.core.scope.notMappable),
    Market: _.difference(filtered, modules.core.scope.notMappable),
    Metric: _.difference(filtered, modules.core.scope.notMappable),
    Objective: _.difference(filtered, ['Audit']),
    OrgGroup: _.difference(filtered, modules.core.scope.notMappable),
    Person: [],
    Policy: _.difference(filtered, ['Audit', 'Policy']),
    Process: _.difference(filtered, modules.core.scope.notMappable),
    Product: _.difference(filtered, modules.core.scope.notMappable),
    ProductGroup: _.difference(filtered, modules.core.scope.notMappable),
    Program: _.difference(allTypes,
      ['Audit', 'Assessment', 'Person']
        .concat(modules.core.notMappable, modules.workflows.notMappable)),
    Project: _.difference(filtered, modules.core.scope.notMappable),
    Regulation: _.difference(filtered, ['Audit', 'Regulation']),
    Risk: _.difference(filtered, ['Audit']),
    Requirement: _.difference(filtered, ['Audit']),
    Standard: _.difference(filtered, ['Audit', 'Standard']),
    System: _.difference(filtered, modules.core.scope.notMappable),
    TaskGroup: _.difference(filtered, ['Audit', 'Person',
      'Workflow', 'Assessment', 'Document']),
    TechnologyEnvironment: _.difference(filtered,
      modules.core.scope.notMappable),
    Threat: _.difference(filtered, ['Audit']),
    Vendor: _.difference(filtered, modules.core.scope.notMappable),
  });

  describe('allowedToUnmap() method', () => {
    beforeEach(() => {
      spyOn(Permission, 'is_allowed_for').and.returnValue(true);
    });

    it('checks that types are mappable', () => {
      let result = Mappings.allowedToUnmap('SourceType', 'TargetType');

      expect(result).toBeFalsy();
      expect(Permission.is_allowed_for).not.toHaveBeenCalled();
    });

    it('checks permissions to update source', () => {
      let result = Mappings.allowedToUnmap('DataAsset', 'AccessGroup');

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for)
        .toHaveBeenCalledWith('update', 'DataAsset');
      expect(Permission.is_allowed_for.calls.count()).toEqual(1);
    });

    it('checks permissions to update target', () => {
      let source = new CanMap({type: 'DataAsset'});
      let target = new CanMap({type: 'AccessGroup'});
      let result = Mappings.allowedToUnmap(source, target);

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for.calls.count()).toEqual(2);
      expect(Permission.is_allowed_for.calls.argsFor(0))
        .toEqual(['update', source]);
      expect(Permission.is_allowed_for.calls.argsFor(1))
        .toEqual(['update', target]);
    });
  });

  describe('getAllowedToUnmapModels() method', () => {
    let modelsForTests = _.difference(allTypes, [
      'TaskGroupTask',
      'CycleTaskGroup',
      'Workflow',
    ]);

    modelsForTests.forEach(function (type) {
      it('returns mappable types for ' + type, function () {
        let expectedModels = unmappingRules[type];
        let result = Mappings.getAllowedToUnmapModels(type);
        let resultModels = _.keys(result);

        expect(expectedModels.sort()).toEqual(resultModels.sort());
      });
    });
  });
});
