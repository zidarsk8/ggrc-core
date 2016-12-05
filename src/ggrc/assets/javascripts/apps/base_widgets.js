/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, _) {
  'use strict';
  /**
   * Tree View Widgets Configuration module
   */
  var allTypes = [
    'AccessGroup', 'Audit', 'Clause', 'Contract', 'Control', 'Assessment',
    'DataAsset', 'Facility', 'Issue', 'Market', 'Objective', 'OrgGroup',
    'Person', 'Policy', 'Process', 'Product', 'Program', 'Project',
    'Regulation', 'Request', 'Section', 'Standard', 'System', 'Vendor'
  ];
  // Items allowed for mapping via snapshot.
  var snapshotWidgetsConfig = GGRC.config.snapshotable_objects || [];
  // Items allowed for relationship mapping
  var excludeMappingConfig = [
    'Assessment',
    'AssessmentTemplate',
    'Request',
    'Issue'
  ];
  // Extra Tree View Widgets require to be rendered on Audit View
  var auditInclusion = [
    'Person',
    'Program'
  ];
  var baseWidgetsByType;

  var filteredTypes = _.difference(allTypes, excludeMappingConfig);
  // Audit is excluded and created a separate logic for it
  baseWidgetsByType = {
    AccessGroup: _.difference(filteredTypes, ['AccessGroup']),
    Audit: [].concat(snapshotWidgetsConfig, excludeMappingConfig,
      auditInclusion).sort(),
    Clause: _.difference(filteredTypes, ['Clause']),
    Contract: _.difference(filteredTypes,
      ['Contract', 'Policy', 'Regulation', 'Standard']),
    Control: filteredTypes,
    Assessment: _.difference(filteredTypes, ['Assessment']),
    DataAsset: filteredTypes,
    Facility: filteredTypes,
    Issue: filteredTypes,
    Market: filteredTypes,
    Objective: filteredTypes,
    OrgGroup: filteredTypes,
    Person: _.difference(filteredTypes, ['Person']),
    Policy: _.difference(filteredTypes,
      ['Contract', 'Policy', 'Regulation', 'Standard']),
    Process: filteredTypes,
    Product: filteredTypes,
    Program: _.difference(filteredTypes, ['Program']),
    Project: filteredTypes,
    Regulation: _.difference(filteredTypes,
      ['Contract', 'Policy', 'Regulation', 'Standard']),
    Section: filteredTypes,
    Standard: _.difference(filteredTypes,
      ['Contract', 'Policy', 'Regulation', 'Standard']),
    System: filteredTypes,
    Vendor: filteredTypes
  };

  GGRC.tree_view = GGRC.tree_view || new can.Map();
  GGRC.tree_view.attr('base_widgets_by_type', baseWidgetsByType);
})(this.GGRC, this._);
