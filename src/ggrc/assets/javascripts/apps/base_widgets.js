/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (GGRC, _) {
  var base_widgets_by_type = {
    "Program": "Issue ControlAssessment Regulation Contract Policy Standard Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Audit": "Issue ControlAssessment Request history Person Program Control",
    "Issue": "ControlAssessment Control Audit Program Regulation Contract Policy Standard Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Issue",
    "ControlAssessment": "Issue Objective Program Regulation Contract Policy Standard Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Regulation": "Program Issue ControlAssessment Section Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person",
    "Policy": "Program Issue ControlAssessment Section Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person",
    "Standard": "Program Issue ControlAssessment Section Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person",
    "Contract": "Program Issue ControlAssessment Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person",
    "Clause": "Contract Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person",
    "Section": "Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person",
    "Objective": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person",
    "Control": "Issue ControlAssessment Request Program Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Person": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Audit Request",
    "OrgGroup": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Vendor": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "System": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Process": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "DataAsset": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Product": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Project": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Facility": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
    "Market": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit"
  };
  base_widgets_by_type = _.mapValues(base_widgets_by_type, function (conf) {
    return conf.split(" ");
  });
  GGRC.tree_view = GGRC.tree_view || {};
  GGRC.tree_view.base_widgets_by_type = base_widgets_by_type;
})(this.GGRC, this._);
