/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as Utils from '../../../plugins/utils/models-utils';
import Mappings from '../mappings';
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

  function getModelsFromGroups(groups, groupNames) {
    let models = [];
    groupNames.forEach(function (groupName) {
      let groupModels = groups[groupName].items.map(function (item) {
        return item.value;
      });
      models = models.concat(groupModels);
    });
    return models;
  }

  Object.keys(modules).forEach(function (module) {
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

  describe('getMappingTypes() method', function () {
    let EXPECTED_GROUPS = ['entities', 'scope', 'governance'];

    let types = allTypes.concat('MultitypeSearch');
    let modelsForTests = _.difference(types, [
      'TaskGroupTask',
      'CycleTaskGroup',
      'Workflow',
    ]);

    modelsForTests.forEach(function (type) {
      it('returns mappable types for ' + type, function () {
        let expectedModels = mappingRules[type];
        let result = Mappings.getMappingTypes(type);
        let resultGroups = Object.keys(result);
        let resultModels = getModelsFromGroups(result, EXPECTED_GROUPS);

        expect(EXPECTED_GROUPS).toEqual(resultGroups);
        expect(expectedModels.sort()).toEqual(resultModels.sort());
      });
    });
  });

  describe('allowedToMap() method', () => {
    beforeEach(() => {
      spyOn(Permission, 'is_allowed_for').and.returnValue(true);
    });

    it('checks that types are mappable', () => {
      spyOn(Mappings, 'getAllowedToMapModels');

      let result = Mappings.allowedToMap('SourceType', 'TargetType');

      expect(result).toBeFalsy();
      expect(Permission.is_allowed_for).not.toHaveBeenCalled();
    });

    it('checks map and externalMap collections', () => {
      spyOn(Mappings, 'getAllowedToMapModels');
      spyOn(Mappings, 'getExternalMapModels');

      Mappings.allowedToMap('SourceType', 'TargetType');

      expect(Mappings.getAllowedToMapModels).toHaveBeenCalled();
      expect(Mappings.getExternalMapModels).toHaveBeenCalled();
    });

    it('checks permissions to update source', () => {
      spyOn(Mappings, 'getAllowedToMapModels').and.returnValue({
        TargetType: {},
      });

      let result = Mappings.allowedToMap('SourceType', 'TargetType');

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for)
        .toHaveBeenCalledWith('update', 'SourceType');
      expect(Permission.is_allowed_for.calls.count()).toEqual(1);
    });

    it('checks permissions to update target', () => {
      spyOn(Mappings, 'getAllowedToMapModels').and.returnValue({
        TargetType: {},
      });

      let source = new can.Map({type: 'SourceType'});
      let target = new can.Map({type: 'TargetType'});
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
      spyOn(Mappings, 'getAllowedToCreateModels').and.returnValue({
        anyType: {},
      });

      let result = Mappings.allowedToCreate('SourceType', 'TargetType');

      expect(result).toBeFalsy();
      expect(Permission.is_allowed_for).not.toHaveBeenCalled();
    });

    it('checks permissions to update source', () => {
      spyOn(Mappings, 'getAllowedToCreateModels').and.returnValue({
        TargetType: {},
      });

      let result = Mappings.allowedToCreate('SourceType', 'TargetType');

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for)
        .toHaveBeenCalledWith('update', 'SourceType');
      expect(Permission.is_allowed_for.calls.count()).toEqual(1);
    });

    it('checks permissions to update target', () => {
      spyOn(Mappings, 'getAllowedToCreateModels').and.returnValue({
        TargetType: {},
      });

      let source = new can.Map({type: 'SourceType'});
      let target = new can.Map({type: 'TargetType'});
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
      spyOn(Mappings, 'getAllowedToUnmapModels').and.returnValue({
        anyType: {},
      });

      let result = Mappings.allowedToUnmap('SourceType', 'TargetType');

      expect(result).toBeFalsy();
      expect(Permission.is_allowed_for).not.toHaveBeenCalled();
    });

    it('checks permissions to update source', () => {
      spyOn(Mappings, 'getAllowedToUnmapModels').and.returnValue({
        TargetType: {},
      });

      let result = Mappings.allowedToUnmap('SourceType', 'TargetType');

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for)
        .toHaveBeenCalledWith('update', 'SourceType');
      expect(Permission.is_allowed_for.calls.count()).toEqual(1);
    });

    it('checks permissions to update target', () => {
      spyOn(Mappings, 'getAllowedToUnmapModels').and.returnValue({
        TargetType: {},
      });

      let source = new can.Map({type: 'SourceType'});
      let target = new can.Map({type: 'TargetType'});
      let result = Mappings.allowedToUnmap(source, target);

      expect(result).toBeTruthy();
      expect(Permission.is_allowed_for.calls.count()).toEqual(2);
      expect(Permission.is_allowed_for.calls.argsFor(0))
        .toEqual(['update', source]);
      expect(Permission.is_allowed_for.calls.argsFor(1))
        .toEqual(['update', target]);
    });
  });

  describe('_prepareCorrectTypeFormat() method', function () {
    let cmsModel = {
      category: 'category',
      title_plural: 'title_plural',
      model_singular: 'model_singular',
    };
    let expectedResult = {
      category: 'category',
      name: 'title_plural',
      value: 'model_singular',
    };

    it('returns specified object', function () {
      let result;
      result = Mappings._prepareCorrectTypeFormat(cmsModel);
      expect(result).toEqual(expectedResult);
    });

    it('converts models plural title to a snake_case', function () {
      let result;
      let cmsModel1 = _.assign({}, cmsModel, {
        title_plural: 'Title Plural',
      });
      result = Mappings._prepareCorrectTypeFormat(cmsModel1);
      expect(result.plural).toEqual(expectedResult.plural);
    });
  });

  describe('addFormattedType() method', function () {
    let groups;
    let type = {
      category: 'category',
    };

    beforeEach(function () {
      groups = {
        governance: {
          items: [],
        },
        category: {
          items: [],
        },
      };
      spyOn(Mappings, '_prepareCorrectTypeFormat')
        .and.returnValue(type);
    });

    it('adds type to governance group if no group with category of this type',
      function () {
        groups.category = undefined;
        spyOn(Utils, 'getModelByType')
          .and.returnValue({
            title_singular: 'title_singular',
          });
        Mappings._addFormattedType('name', groups);
        expect(groups.governance.items[0]).toEqual(type);
      });

    it('adds type to group of category of this type if this group exist',
      function () {
        groups.governance = undefined;
        spyOn(Utils, 'getModelByType')
          .and.returnValue({
            title_singular: 'title_singular',
          });
        Mappings._addFormattedType('name', groups);
        expect(groups[type.category].items[0]).toEqual(type);
      });

    it('does nothing if cmsModel is not defined', function () {
      spyOn(Utils, 'getModelByType');
      Mappings._addFormattedType('name', groups);
      expect(groups.governance.items.length).toEqual(0);
      expect(groups[type.category].items.length).toEqual(0);
    });
    it('does nothing if singular title of cmsModel is not defined',
      function () {
        spyOn(Utils, 'getModelByType')
          .and.returnValue({});
        Mappings._addFormattedType('name', groups);
        expect(groups.governance.items.length).toEqual(0);
        expect(groups[type.category].items.length).toEqual(0);
      });
  });
});
