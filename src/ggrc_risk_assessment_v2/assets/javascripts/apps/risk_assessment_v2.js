/*
 * Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: silas@reciprocitylabs.com
 * Maintained By: silas@reciprocitylabs.com
 */


(function($, CMS, GGRC) {
  var RiskAssessmentV2Extension = {};

    // Insert risk mappings to all gov/business object types
    var _risk_object_types = [
      "Program",
      "Regulation", "Standard", "Policy", "Contract",
      "Objective", "Control", "Section", "Clause",
      "System", "Process",
      "DataAsset", "Facility", "Market", "Product", "Project"
    ];

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
        CustomFilter = GGRC.MapperHelpers.CustomFilter,
        Reify = GGRC.MapperHelpers.Reify,
        Search = GGRC.MapperHelpers.Search;

    // Add mappings for risk objects
    ////$.extend(GGRC.Mappings, {
    var mappings = {
        Risk: {
          _canonical : { objects : _risk_object_types },
          objects: Proxy(
            null, "object", "RiskObject", "risk", "risk_objects"),
        }
    ////});
    };

    can.each(_risk_object_types, function(type) {
      mappings[type] = {};
      mappings[type]._canonical = { "risks" : "Risk" };
      mappings[type].risks = new GGRC.ListLoaders.ProxyListLoader(
        "RiskObject", "object", "risk", "risk_objects", null);
    });
    new GGRC.Mappings("ggrc_risk_assessment_v2", mappings);
};
/*
  // Construct and add JoinDescriptors for risk_assessment_v2 extension
  RiskAssessmentV2Extension.init_join_descriptors = function init_join_descriptors() {
    var join_descriptor_arguments = [
    ];
  };
*/

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
          "info", "objects"
        ],
        objects_widget_descriptor,
        object = GGRC.page_instance(),
        object_descriptors = {};

    can.each(GGRC.WidgetList.get_current_page_widgets(), function(descriptor, name) {
      if (~new_default_widgets.indexOf(name))
        risk_widget_descriptors[name] = descriptor;
    });

    GGRC.register_hook(
        "ObjectNav.Actions",
        GGRC.mustache_path + "/dashboard/object_nav_actions");

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

    objects_widget_descriptor = {
      content_controller: CMS.Controllers.TreeView,
      content_controller_selector: "ul",
      widget_initial_content: '<ul class="tree-structure new-tree multitype-tree"></ul>',
      widget_id: "objects",
      widget_name: "Objects",
      widget_icon: "object",
      content_controller_options: {
        child_options: [],
        draw_children: false,
        parent_instance: object,
        model: can.Model.Cacheable,
        mapping: "objects",
        footer_view: GGRC.mustache_path + "/risk_objects/tree_footer.mustache"
      }
    };

    risk_widget_descriptors.objects = objects_widget_descriptor;

    new GGRC.WidgetList("ggrc_risk_assessment_v2", { Risk: risk_widget_descriptors });
  };

  GGRC.register_hook("LHN.Sections", GGRC.mustache_path + "/dashboard/lhn_risk_assessment_v2");

  RiskAssessmentV2Extension.init_mappings();

})(this.can.$, this.CMS, this.GGRC);
