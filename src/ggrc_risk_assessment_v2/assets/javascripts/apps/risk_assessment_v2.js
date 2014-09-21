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
    ], related_object_descriptors = {};

  // Register `risk_assessment_v2` extension with GGRC
  GGRC.extensions.push(RiskAssessmentV2Extension);

  RiskAssessmentV2Extension.name = "risk_assessment_v2";

  // Register Risk Assessment models for use with `infer_object_type`
  RiskAssessmentV2Extension.object_type_decision_tree = function() {
    return {
      "risk": CMS.Models.Risk,
      "threat_actor": CMS.Models.ThreatActor
    };
  };

  // Configure mapping extensions for ggrc_risk_assessment_v2
  RiskAssessmentV2Extension.init_mappings = function init_mappings() {
    var Proxy = GGRC.MapperHelpers.Proxy,
        Direct = GGRC.MapperHelpers.Direct,
        Cross = GGRC.MapperHelpers.Cross,
        CustomFilter = GGRC.MapperHelpers.CustomFilter,
        Reify = GGRC.MapperHelpers.Reify,
        Search = GGRC.MapperHelpers.Search,
        TypeFilter = GGRC.MapperHelpers.TypeFilter,
        Multi = GGRC.MapperHelpers.Multi;

    // Add mappings for risk objects
    var mappings = {
        related: {
          _canonical: {
            "related_objects_as_source": _risk_object_types
          },
          related_objects_as_source: Proxy(
            null, "destination", "Relationship", "source", "related_destinations"),
          related_objects_as_destination: Proxy(
            null, "source", "Relationship", "destination", "related_sources"),
          related_objects: Multi(["related_objects_as_source", "related_objects_as_destination"]),
          related_data_assets: TypeFilter("related_objects", "DataAsset"),
          related_facilities: TypeFilter("related_objects", "Facility"),
          related_markets: TypeFilter("related_objects", "Market"),
          related_processes: TypeFilter("related_objects", "Process"),
          related_products: TypeFilter("related_objects", "Product"),
          related_projects: TypeFilter("related_objects", "Project"),
          related_systems: TypeFilter("related_objects", "System"),
          related_controls: TypeFilter("related_objects", "Control"),
          related_clauses: TypeFilter("related_objects", "Clause"),
          related_objectives: TypeFilter("related_objects", "Objecitve"),
          related_sections: TypeFilter("related_objects", "Section"),
          related_regulations: TypeFilter("related_objects", "Regulation"),
          related_contracts: TypeFilter("related_objects", "Contract"),
          related_policies: TypeFilter("related_objects", "Policy"),
          related_standards: TypeFilter("related_objects", "Standard"),
          related_programs: TypeFilter("related_objects", "Program"),
        },
        Risk: {
          _mixins: ['related']
        },
        ThreatActor: {
          _mixins: ['related']
        }
    };

    can.each(_risk_object_types, function(type) {
      mappings[type] = {};
      mappings[type]._canonical = { "risks" : "Risk" };
      mappings[type].risks = new GGRC.ListLoaders.ProxyListLoader(
        "RiskObject", "object", "risk", "risk_objects", null);

      mappings[type].related_threat_actors = TypeFilter("related_objects", "ThreatActor")
    });
    new GGRC.Mappings("ggrc_risk_assessment_v2", mappings);
};

  // Override GGRC.extra_widget_descriptors and GGRC.extra_default_widgets
  // Initialize widgets for risk page
  RiskAssessmentV2Extension.init_widgets = function init_widgets() {
    var page_instance = GGRC.page_instance();

    // Init widget descriptors:
    can.each(_risk_object_types, function(model_name){
      var model = CMS.Models[model_name];
      related_object_descriptors[model_name] = {
        content_controller: CMS.Controllers.TreeView,
        content_controller_selector: "ul",
        widget_initial_content: '<ul class="tree-structure new-tree multitype-tree"></ul>',
        widget_id: model.table_plural,
        widget_name: model.model_plural,
        widget_icon: model.table_singular,
        content_controller_options: {
          child_options: [],
          draw_children: false,
          parent_instance: page_instance,
          model: model,
          mapping: "related_" + model.table_plural,
        }
      }
    });

    if (page_instance instanceof CMS.Models.Risk) {
      RiskAssessmentV2Extension.init_widgets_for_risk_page();
    }
    if (page_instance instanceof CMS.Models.ThreatActor) {
      RiskAssessmentV2Extension.init_widgets_for_threat_actor_page();
    }
  };

  RiskAssessmentV2Extension.init_widgets_for_risk_page =
      function init_widgets_for_risk_page() {
    new GGRC.WidgetList("ggrc_risk_assessment_v2", { Risk: related_object_descriptors });
  };

  RiskAssessmentV2Extension.init_widgets_for_threat_actor_page =
      function init_widgets_for_threat_actor_page() {
    new GGRC.WidgetList("ggrc_risk_assessment_v2", { ThreatActor: related_object_descriptors });
  };



  GGRC.register_hook("LHN.Sections", GGRC.mustache_path + "/dashboard/lhn_risk_assessment_v2");

  RiskAssessmentV2Extension.init_mappings();

})(this.can.$, this.CMS, this.GGRC);
