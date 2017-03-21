/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Models.MapperModel', function () {
  'use strict';

  var MapperModel;
  var allTypes = [];
  var notMappableModels = [];
  var modules = {
    core: {
      models: [
        'AccessGroup',
        'Assessment',
        'AssessmentTemplate',
        'Audit',
        'Clause',
        'Contract',
        'Control',
        'DataAsset',
        'Facility',
        'Issue',
        'Market',
        'Objective',
        'OrgGroup',
        'Person',
        'Policy',
        'Process',
        'Product',
        'Program',
        'Project',
        'Regulation',
        'Section',
        'Standard',
        'System',
        'Vendor',
        'Risk',
        'Threat'
      ],
      notMappable: ['Assessment', 'Issue', 'AssessmentTemplate']
    },
    risk_assessments: {
      models: ['RiskAssessment'],
      notMappable: ['RiskAssessment']
    },
    workflows: {
      models: [
        'TaskGroup',
        'Workflow',
        'CycleTaskEntry',
        'CycleTaskGroupObjectTask',
        'CycleTaskGroupObject',
        'CycleTaskGroup'
      ],
      notMappable: [
        'CycleTaskEntry',
        'CycleTaskGroupObjectTask',
        'CycleTaskGroupObject',
        'CycleTaskGroup'
      ]
    }
  };
  var directives = ['Contract', 'Policy', 'Regulation', 'Standard'];
  var mappingRules;
  var filtered;
  var treeViewSettingsBackup;

  function getModelsFromGroups(groups, groupNames) {
    var models = [];
    groupNames.forEach(function (groupName) {
      var groupModels = groups[groupName].items.map(function (item) {
        return item.singular;
      });
      models = models.concat(groupModels);
    });
    return models;
  }

  Object.keys(modules).forEach(function (module) {
    allTypes = allTypes.concat(modules[module].models);
    notMappableModels = notMappableModels.concat(modules[module].notMappable);
  });

  filtered = _.difference(allTypes, notMappableModels);

  mappingRules = {
    AccessGroup: _.difference(filtered, ['AccessGroup']),
    Assessment: _.difference(filtered, ['Audit', 'Person', 'Program', 'Project',
      'TaskGroup', 'Workflow']),
    AssessmentTemplate: _.difference(filtered, ['Audit', 'Person', 'Program',
      'Project', 'TaskGroup', 'Workflow']),
    Audit: _.difference(filtered, ['Audit', 'Person', 'Program', 'Project',
      'TaskGroup', 'Workflow']),
    Clause: _.difference(filtered, ['Clause']),
    Contract: _.difference(filtered, directives),
    Control: filtered,
    CycleTaskGroupObjectTask: _.difference(filtered, ['Person',
      'TaskGroup', 'Workflow']),
    DataAsset: filtered,
    Facility: filtered,
    Issue: _.difference(filtered, ['Audit', 'Person', 'Program', 'Project',
      'TaskGroup', 'Workflow']),
    Market: filtered,
    Objective: filtered,
    OrgGroup: filtered,
    Person: _.difference(filtered, ['Person', 'Audit', 'TaskGroup',
      'Workflow']),
    Policy: _.difference(filtered, directives),
    Process: filtered,
    Product: filtered,
    Program: _.difference(allTypes, ['Program'].concat(modules.core.notMappable,
      modules.workflows.notMappable)),
    Project: filtered,
    Regulation: _.difference(filtered, directives),
    Risk: filtered,
    RiskAssessment: [],
    Section: filtered,
    Standard: _.difference(filtered, directives),
    System: filtered,
    TaskGroup: _.difference(filtered, ['Audit', 'Person',
      'TaskGroup', 'Workflow']),
    Threat: filtered,
    Vendor: filtered
  };

  beforeAll(function () {
    treeViewSettingsBackup = new can.Map(GGRC.tree_view);
    // init all modules
    can.each(GGRC.extensions, function (extension) {
      if (modules[extension.name] && extension.init_widgets) {
        extension.init_widgets();
      }
    });
  });

  afterAll(function () {
    GGRC.tree_view = treeViewSettingsBackup;
  });

  beforeEach(function () {
    MapperModel = new GGRC.Models.MapperModel();
  });

  describe('initTypes() method', function () {
    var initTypes;
    var EXPECTED_GROUPS = ['entities', 'business', 'governance'];
    var modelsForTests = _.difference(allTypes, [
      'CycleTaskEntry',
      'CycleTaskGroup',
      'CycleTaskGroupObject',
      'Workflow'
    ]);

    beforeEach(function () {
      initTypes = MapperModel.initTypes.bind(MapperModel);
      MapperModel.attr('search_only', false);
    });

    modelsForTests.forEach(function (type) {
      it('returns mappable types for ' + type, function () {
        var expectedModels = mappingRules[type];
        var result = initTypes(type);
        var resultGroups = Object.keys(result);
        var resultModels = getModelsFromGroups(result, EXPECTED_GROUPS);

        expect(EXPECTED_GROUPS).toEqual(resultGroups);
        expect(expectedModels.sort()).toEqual(resultModels.sort());
      });
    });
  });
});
