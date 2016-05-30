/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: dan@reciprocitylabs.com
 * Maintained By: dan@reciprocitylabs.com
 */

(function($, CMS, GGRC) {
  var RiskAssessmentsExtension = {},
      _risk_assessments_object_types = ["Program"];
  GGRC.extensions.push(RiskAssessmentsExtension);

  RiskAssessmentsExtension.name = "risk_assessments";

  // Register RA models for use with `infer_object_type`
  RiskAssessmentsExtension.object_type_decision_tree = function() {
    return {
      "risk_assessment": CMS.Models.RiskAssessment
    };
  };

  CMS.Models.Program.attributes.risk_assessments = "CMS.Models.RiskAssessment.stubs";

  // Configure mapping extensions for ggrc_risk_assessments
  RiskAssessmentsExtension.init_mappings = function init_mappings() {
    var Proxy = GGRC.MapperHelpers.Proxy,
        Direct = GGRC.MapperHelpers.Direct,
        Cross = GGRC.MapperHelpers.Cross,
        Multi = GGRC.MapperHelpers.Multi,
        CustomFilter = GGRC.MapperHelpers.CustomFilter,
        Reify = GGRC.MapperHelpers.Reify,
        Search = GGRC.MapperHelpers.Search;

        var mappings = {
          Program: {
            _canonical: {
              risk_assessments: "RiskAssessment"
            },
            risk_assessments: Direct(
              "RiskAssessment", "program", "risk_assessments"),
          },
          RiskAssessment: {
            documents: Proxy(
              "Document", "document", "ObjectDocument", "documentable", "object_documents"),
          },
        };
        new GGRC.Mappings("ggrc_risk_assessments", mappings);
  };

  // Override GGRC.extra_widget_descriptors and GGRC.extra_default_widgets
  // Initialize widgets for risk assessment page
  RiskAssessmentsExtension.init_widgets = function init_widgets() {
    var descriptor = {},
        page_instance = GGRC.page_instance(),
        tree_widgets = GGRC.tree_view.base_widgets_by_type;

    _.each(_risk_assessments_object_types, function (type) {
      if (!type || !tree_widgets[type]) {
        return;
      }
      tree_widgets[type] = tree_widgets[type].concat(["RiskAssessment"]);
    });
    if (page_instance && ~can.inArray(page_instance.constructor.shortName, _risk_assessments_object_types)) {
      descriptor[page_instance.constructor.shortName] = {
        risk_assessments: {
          widget_id: "risk_assessments",
          widget_name: "Risk Assessments",
          content_controller: GGRC.Controllers.TreeView,
          content_controller_options: {
            mapping: "risk_assessments",
            parent_instance: page_instance,
            model: CMS.Models.RiskAssessment,
            show_view: GGRC.mustache_path + "/risk_assessments/tree.mustache",
            draw_children: true,
          }
        }
      };
    }
    new GGRC.WidgetList("ggrc_risk_assessments", descriptor);
  };

  RiskAssessmentsExtension.init_mappings();

})(this.can.$, this.CMS, this.GGRC);
