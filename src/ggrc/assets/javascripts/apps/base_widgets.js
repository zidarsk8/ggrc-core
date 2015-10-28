/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (GGRC, _) {
  var base_widgets_by_type = {
    "Program": "Issue ControlAssessment Regulation Contract Policy Standard Objective Control System Process DataAsset AccessGroup Product Project Facility Market OrgGroup Vendor Person Audit Clause Section",
      "Audit": "Issue ControlAssessment Request history Person Program Control",
      "Issue": "ControlAssessment Control Audit Program Regulation Contract Policy Standard Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Issue AccessGroup Clause Section",
      "ControlAssessment": "Issue Objective Program Clause Regulation Contract Policy Standard Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit Request AccessGroup Section",
      "Regulation": "Program Issue ControlAssessment Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person AccessGroup",
      "Policy": "Program Issue ControlAssessment Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person AccessGroup",
      "Standard": "Program Issue ControlAssessment Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person AccessGroup",
      "Contract": "Program Issue ControlAssessment Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person AccessGroup Section",
      "Clause": "Contract Objective ControlAssessment Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person AccessGroup Section Policy Regulation Standard Program Audit",
      "Section": "Objective Control ControlAssessment System Process DataAsset Product Project Facility Market OrgGroup Vendor AccessGroup Person Policy Regulation Standard Contract Clause Program Audit",
      "Objective": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person AccessGroup",
      "Control": "Issue ControlAssessment Request Program Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "Person": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Audit Request AccessGroup",
      "OrgGroup": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "Vendor": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "System": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "Process": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "DataAsset": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "AccessGroup": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit",
      "Product": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "Project": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "Facility": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup",
      "Market": "Program Issue ControlAssessment Regulation Contract Policy Standard Section Clause Objective Control System Process DataAsset Product Project Facility Market OrgGroup Vendor Person Audit AccessGroup"
  };
  base_widgets_by_type = _.mapValues(base_widgets_by_type, function (conf) {
    return conf.split(" ");
  });
  GGRC.tree_view = GGRC.tree_view || {};
  GGRC.tree_view.base_widgets_by_type = base_widgets_by_type;
})(this.GGRC, this._);
