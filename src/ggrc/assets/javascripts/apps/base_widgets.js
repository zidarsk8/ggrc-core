/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (GGRC, _) {
  var base_widgets_by_type = {
    AccessGroup: 'Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Audit: 'AccessGroup Clause Contract Control Assessment AssessmentTemplate DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Clause: 'AccessGroup Audit Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Section Standard System Vendor',
    Contract: 'AccessGroup Audit Clause Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Process Product Program Project Request Section System Vendor',
    Control: 'AccessGroup Audit Clause Contract Control Assessment DataAsset Facility Issue Market Objective OrgGroup Person Policy Process Product Program Project Regulation Request Request Section Standard System Vendor',
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
  base_widgets_by_type = _.mapValues(base_widgets_by_type, function (conf) {
    return conf.split(' ');
  });
  GGRC.tree_view = GGRC.tree_view || {};
  GGRC.tree_view.base_widgets_by_type = base_widgets_by_type;
})(this.GGRC, this._);
