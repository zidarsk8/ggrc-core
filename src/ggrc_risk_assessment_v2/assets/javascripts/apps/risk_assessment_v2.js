/*
 * Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: silas@reciprocitylabs.com
 * Maintained By: silas@reciprocitylabs.com
 */


(function($, CMS, GGRC) {
  var RiskAssessmentV2Extension = {};

  // Register `risk_assessment_v2` extension with GGRC
  GGRC.extensions.push(RiskAssessmentV2Extension);

  RiskAssessmentV2Extension.name = "risk_assessment_v2";

  // Register Risk Assessment models for use with `infer_object_type`
  RiskAssessmentV2Extension.object_type_decision_tree = function() {
    return {
      "risk": CMS.Models.Risk,
    };
  };

  // Configure mapping extensions for ggrc_risk_assessment_v2
  RiskAssessmentV2Extension.init_mappings = function init_mappings() {
    var Proxy = GGRC.MapperHelpers.Proxy,
        Direct = GGRC.MapperHelpers.Direct,
        Cross = GGRC.MapperHelpers.Cross,
        CustomFilter = GGRC.MapperHelpers.CustomFilter;
  };

  // Construct and add JoinDescriptors for risk_assessment_v2 extension
  RiskAssessmentV2Extension.init_join_descriptors = function init_join_descriptors() {
    var join_descriptor_arguments = [
    ];
  };


  // Override GGRC.extra_widget_descriptors and GGRC.extra_default_widgets
  // Initialize widgets for risk page
  RiskAssessmentV2Extension.init_widgets = function init_widgets() {
    var page_instance = GGRC.page_instance();

    // More cases to handle later
    if (page_instance instanceof CMS.Models.Risk) {
      RiskAssessmentV2Extension.init_widgets_for_risk_page();
    }
  };

  RiskAssessmentV2Extension.init_widgets_for_risk_page =
      function init_widgets_for_risk_page() {

    var risk_widget_descriptors = {},
        new_default_widgets = [
          "info"
        ];

    can.each(GGRC.WidgetList.get_current_page_widgets(), function(descriptor, name) {
      if (~new_default_widgets.indexOf(name))
        risk_widget_descriptors[name] = descriptor;
    });

    $.extend(
      true,
      risk_widget_descriptors,
      {
        info: {
          content_controller: GGRC.Controllers.InfoWidget,
          content_controller_options: {
            widget_view: GGRC.mustache_path + "/risks/info.mustache"
          }
        }
      }
    );

    new GGRC.WidgetList("ggrc_risk_assessment_v2", { Risk: risk_widget_descriptors });
  };

  GGRC.register_hook("LHN.Sections", GGRC.mustache_path + "/dashboard/lhn_risk_assessment_v2");

  RiskAssessmentV2Extension.init_mappings();
  RiskAssessmentV2Extension.init_join_descriptors();

})(this.can.$, this.CMS, this.GGRC);
