/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require controllers/quick_search_controller
(function(namespace, $) {

var RELATIONSHIP_TYPES = {
  "DataAsset":  {
    "Process": ["data_asset_has_process"]
    , "DataAsset": ["data_asset_relies_upon_data_asset"]
    , "Facility": ["data_asset_relies_upon_facility"]
    , "System": ["data_asset_relies_upon_system"]
  }, "Facility": {
    "Process": ["facility_has_process"]
    , "DataAsset": ["facility_relies_upon_data_asset"]
    , "Facility": ["facility_relies_upon_facility"]
    , "System": ["facility_relies_upon_system"]
  }, "Market": {
    "Process": ["market_has_process"]
    , "Market": ["market_includes_market"]
    , "DataAsset": ["market_relies_upon_data_asset"]
    , "Facility": ["market_relies_upon_facility"]
    , "System": ["market_relies_upon_system"]
  }, "OrgGroup": {
      "Process": ["org_group_has_process", "org_group_is_responsible_for_process"]
    , "OrgGroup": ["org_group_is_affiliated_with_org_group", "org_group_is_responsible_for_org_group", "org_group_relies_upon_org_group"]
    , "DataAsset": ["org_group_is_responsible_for_data_asset", "org_group_relies_upon_data_asset"]
    , "Facility": ["org_group_is_responsible_for_facility", "org_group_relies_upon_facility"]
    , "Market": ["org_group_is_responsible_for_market"]
    , "Product": ["org_group_is_responsible_for_product"]
    , "Project": ["org_group_is_responsible_for_project"]
    , "System": ["org_group_is_responsible_for_system", "org_group_relies_upon_system"]
  }, "Product": {
    "Process": ["product_has_process"]
    , "Product": ["product_is_affiliated_with_product", "product_relies_upon_product"]
    , "Market": ["product_is_sold_into_market"]
    , "DataAsset": ["product_relies_upon_data_asset"]
    , "Facility": ["product_relies_upon_facility"]
    , "System": ["product_relies_upon_system"]
  }, "Program": {
    "DataAsset": ["program_applies_to_data_asset"]
    , "Facility": ["program_applies_to_facility"]
    , "Market": ["program_applies_to_market"]
    , "OrgGroup": ["program_applies_to_org_group"]
    , "Process": ["program_applies_to_process"]
    , "Product": ["program_applies_to_product"]
    , "Project": ["program_applies_to_project"]
    , "System": ["program_applies_to_system"]
  }, "Project": {
    "Process": ["project_has_process"]
    , "DataAsset": ["project_relies_upon_data_asset", "project_targets_data_asset"]
    , "Facility": ["project_relies_upon_facility", "project_targets_facility"]
    , "System": ["project_relies_upon_system"]
    , "Market": ["project_targets_market"]
    , "OrgGroup": ["project_targets_org_group"]
    , "Product": ["project_targets_product"]
  }, "Risk": {
    "DataAsset": ["risk_is_a_threat_to_data_asset"]
    , "Facility": ["risk_is_a_threat_to_facility"]
    , "Market": ["risk_is_a_threat_to_market"]
    , "OrgGroup": ["risk_is_a_threat_to_org_group"]
    , "Process": ["risk_is_a_threat_to_process"]
    , "Product": ["risk_is_a_threat_to_product"]
    , "Project": ["risk_is_a_threat_to_project"]
    , "System": ["risk_is_a_threat_to_system"]
}};

GGRC.RELATIONSHIP_TYPES = RELATIONSHIP_TYPES;

$(function() {

  $(".recent").ggrc_controllers_recently_viewed();

  function bindQuickSearch(ev, opts) {

    var $qs = $(this).uniqueId();
    var obs = new can.Observe();
    if($qs.find("ul.tree-structure").length) {
      return;
    }
    $qs.bind("keypress", "input.widgetsearch", function(ev) {
      if(ev.which === 13)
        obs.attr("value", $(ev.target).val());
    });
    can.getObject("Instances", CMS.Controllers.QuickSearch, true)[$qs.attr("id")] = 
     $qs.find(".lhs-nav:not(.recent), section.content")
      .cms_controllers_quick_search(can.extend({
        observer : obs
        , spin : $qs.is(":not(section)")
      }, opts)).control(CMS.Controllers.QuickSearch);

  }
  $("section.widget-tabs").each(function() {
    bindQuickSearch.call(this, {}, {});
  });//get anything that exists on the page already.

  $(".lhs").each(function() {
    bindQuickSearch.call(this, {}, {
      list_view : GGRC.mustache_path + "/base_objects/search_result.mustache"
      , tooltip_view : GGRC.mustache_path + "/base_objects/extended_info.mustache"
      , spin : false
      , tab_selector : 'ul.top-level > li > a'
      // , tab_href_attr : [ "href", "data-tab-href" ]
      , tab_target_attr : "href"
      // , tab_model_attr : [ "data-model", "data-object-singular" ]
      , limit : 6
    });
  });
  //Then listen for new ones
  $(document.body).on("click", ".quick-search:not(:has(.cms_controllers_quick_search)), section.widget-tabs:not(:has(.cms_controllers_quick_search))", bindQuickSearch);

  $(document.body).on("click", ".bar-v", function(ev) {
    $("#lhs").toggleClass("lhs-closed");
    resize_areas();
    if ( $("#lhs").hasClass("lhs-closed") ) {
      $(".header-content.affix").css("left","48px");
    } else {
      $(".header-content.affix").css("left","248px");
    }
    
  });

  $(document.body).on("click", ".map-to-page-object", function(ev) {
    var inst = $(ev.target).closest("[data-model], :data(model)").data("model")
    , page_model = GGRC.infer_object_type(GGRC.page_object)
    , page_instance = GGRC.make_model_instance(GGRC.page_object)
    , link = page_model.links_to[inst.constructor.model_singular]
    , params = {};

    if(typeof link === "string") {
      link = GGRC.Models[link] || CMS.Models[link];
    }

    function triggerFlash() {
      $(ev.target).trigger(
        "ajax:flash"
        , {
          success : [
            "Mapped"
            , inst.constructor.title_singular
            , "<strong>"
            , inst.title
            , "</strong> to"
            , page_model.title_singular
            , "<strong>"
            , page_instance.title
            , "</strong>"
            ].join(" ")
          });
    }

    if(can.isPlainObject(link)) {

      $("<div id='relationship_type_modal' class='modal hide'>").appendTo(document.body)
        .modal_form({}, ev.target)
        .ggrc_controllers_modals({
          new_object_form : true
          , button_view : GGRC.Controllers.Modals.BUTTON_VIEW_SAVE_CANCEL
          , model : CMS.Models.Relationship
          , page_object : page_instance
          , related_object : inst
          , relationships : can.map(RELATIONSHIP_TYPES[page_model.model_singular][inst.constructor.model_singular], function(v) {
            return {id : v, name : v.replace(/_/g, " ") };
          })
          , find_params : {
            source : page_instance
            , destination : inst
            , context : page_instance.context || { id : null }
          }
          , modal_title : "Select Relationship Type"
          , content_view : GGRC.mustache_path + "/base_objects/map_related_modal_content.mustache"
        })
        .one("modal:success", triggerFlash);
    } else {
      params[page_model.root_object] = { id : page_instance.id };
      params[inst.constructor.root_object] = { id : inst.id };
      params.context = page_instance.context || { id : null };
      new link(params).save().done(triggerFlash);
    }

  });

});

})(this, jQuery);
