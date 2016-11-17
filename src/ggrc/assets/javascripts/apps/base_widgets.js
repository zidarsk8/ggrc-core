/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (GGRC, can) {
  'use strict';
  /**
   * Tree View Widgets Configuration module
   * NOTE: should replaced with some back-end configuration JSON
   */
  // Items allowed for mapping via snapshot.
  // NOTE: 'Risk' and 'Threat' Models has no mapping configuration with Audit!!! Need to be double checked
  var snapshotWidgetsConfig = [
    'AccessGroup',
    'Clause', 'Contract',
    'Control',
    'DataAsset',
    'Facility', 'Market',
    'Objective',
    'OrgGroup',
    'Policy',
    'Process',
    'Product',
    'Regulation',
    'Section',
    'Standard',
    'System',
    'Vendor',
    'Risk',
    'Threat'];
  // Items allowed for relationship mapping
  var directMappingConfig = [
    'Assessment',
    'AssessmentTemplate',
    'Issue',
    'Request'
  ];
  // Extra Tree View Widgets require to be rendered on Audit View
  var auditInclusion = [
    'Person',
    'Program'
  ];
  // Audit is excluded and created a separate logic for it
  var baseWidgetsConfig = {
    AccessGroup: 'Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor Snapshot',
    Clause: 'AccessGroup Audit Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor Snapshot',
    Contract: 'AccessGroup Audit Clause Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Process Product Program Project Request Section System Vendor Snapshot',
    Control: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Request Section Standard System Vendor Snapshot',
    Assessment: 'AccessGroup Audit Clause Contract Control DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Request Section Standard System Vendor',
    DataAsset: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Facility: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Issue: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Market: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Objective: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    OrgGroup: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Person: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Policy Process Product Program Project Regulation Request Request Section Standard System Vendor',
    Policy: 'AccessGroup Audit Clause Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Process Product Program Project Request Section System Vendor',
    Process: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Product: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Program: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Project Regulation Request Section Standard System Vendor',
    Project: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Regulation: 'AccessGroup Audit Clause Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Process Product Program Project Request Section System Vendor',
    Request: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Section: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Standard: 'AccessGroup Audit Clause Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Process Product Program Project Request Section System Vendor',
    System: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Vendor: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor'
  };
  var baseWidgets = {};
  // Should be replaced in a future
  baseWidgets.Audit = []
    .concat(snapshotWidgetsConfig, directMappingConfig, auditInclusion)
    .sort();

  Object.keys(baseWidgetsConfig)
    .forEach(function (key) {
      baseWidgets[key] = baseWidgetsConfig[key].split(' ').sort();
    });
  GGRC.tree_view = GGRC.tree_view || new can.Map();
  GGRC.tree_view.attr('base_widgets_by_type', baseWidgets);
})(window.GGRC, window.can);
