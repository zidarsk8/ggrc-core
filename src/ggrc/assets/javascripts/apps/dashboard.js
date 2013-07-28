/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require controllers/resize_widgets_controller
//= require controllers/sortable_widgets_controller
//= require controllers/dashboard_widgets
//= require models/simple_models
//= require controls/control
//= require sections/section
//= require pbc/system

(function(namespace, $) {

var model_descriptors = {
  "program" : {
    model : CMS.Models.Program
    , object_type : "program"
    , object_category : "governance"
    , object_route : "programs"
    , object_display : "Programs"
    , tooltip_view : "/static/mustache/programs/object_tooltip.mustache"
  }
  , "directive" : {
    model : CMS.Models.Directive
    , object_type : "directive"
    , object_category : "governance"
    , object_route : "directives"
    , object_display : "Regulations/Policies/Contracts"
  }
  , "regulation" : {
    model : CMS.Models.Regulation
    , object_type : "regulation"
    , object_category : "governance"
    , object_route : "directives"
    , object_display : "Regulations"
  }
  , "policy" : {
    model : CMS.Models.Policy
    , object_type : "policy"
    , object_category : "governance"
    , object_route : "directives"
    , object_display : "Policies"
  }
  , "contract" : {
    model : CMS.Models.Contract
    , object_type : "contract"
    , object_category : "governance"
    , object_route : "directives"
    , object_display : "Contracts"
  }
  , "org_group" : {
    model : CMS.Models.OrgGroup
    , object_type : "org_group"
    , object_category : "business"
    , object_route : "org_groups"
    , object_display : "Org Groups"
  }
  , "project" : {
    model : CMS.Models.Project
    , object_type : "project"
    , object_category : "business"
    , object_route : "projects"
    , object_display : "Projects"
  }
  , "facility" : {
    model : CMS.Models.Facility
    , object_type : "facility"
    , object_category : "business"
    , object_route : "facilities"
    , object_display : "Facilities"
  }
  , "product" : {
    model : CMS.Models.Product
    , object_type : "product"
    , object_category : "business"
    , object_route : "products"
    , object_display : "Products"
  }
  , "data_asset" : {
    model : CMS.Models.DataAsset
    , object_type : "data_asset"
    , object_category : "business"
    , object_route : "data_assets"
    , object_display : "Data Assets"
  }
  , "market" : {
    model : CMS.Models.Market
    , object_type : "market"
    , object_category : "business"
    , object_route : "markets"
    , object_display : "Markets"
  }
  , "process" : {
    model : CMS.Models.Process
    , object_type : "process"
    , object_category : "business"
    , object_route : "systems"
    , object_display : "Processes"
  }
  , "system" : {
    model : CMS.Models.StrictSystem
    , object_type : "system"
    , object_category : "business"
    , object_route : "systems"
    , object_display : "Systems"
  }
  , "control" : {
    model : CMS.Models.Control
    , object_type : "control"
    , object_category : "governance"
    , object_route : "controls"
    , object_display : "Controls"
  }
  , "risky_attribute" : {
    model : CMS.Models.RiskyAttribute
    , object_type : "risky_attribute"
    , object_category : "risk"
    , object_route : "risky_attributes"
    , object_display : "Risky Attributes"
  }
  , "risk" : {
    model : CMS.Models.Risk
    , object_type : "risk"
    , object_category : "risk"
    , object_route : "risks"
    , object_display : "Risks"
  }
  //section isn't a widget but the descriptors are also useful for notes controller
  , "section" : {
    model : CMS.Models.Section
    , object_type : "section"
    , object_route : "sections"
    , object_category : "governance"
  }
  , "system_process" : {
    model : CMS.Models.System
    , object_type : "system_process"
    , object_category : "business"
    , object_route : "systems"
    , object_display : "Systems/Processes"
    , widget_view : "/static/mustache/systems/object_widget.mustache"
  }
  , "sectionslug" : {
    model : CMS.Models.SectionSlug
    , object_type : "section"
    , object_route : "sections"
    , object_category : "governance"
  }
};

dashboard_menu_spec = [
  { title : "Governance / Compliance"
  , objects: [ "regulation", "policy", "contract", "control" ]
  },
  { title : "Asset / Business"
  , objects: [ "system", "process", "org_group", "project"
             , "facility", "product", "data_asset", "market" ]
  },
  /*{ title : "Risk"
  , objects: [ "risky_attributes", "risk" ]
  }*/
]

//function make_admin_menu(widget_descriptors) {
var admin_menu_spec = [
  { title : "Admin"
  , objects: [ "roles", "events", "people" ]
  }
]

$(function() {

  CMS.Models.DisplayPrefs.findAll().done(function(data) {

    function bindResizer(ev) {
        can.getObject("Instances", CMS.Controllers.ResizeWidgets, true)[this.id] = 
         $(this)
          .cms_controllers_resize_widgets({
            model : data[0]
            , minimum_widget_height : (/dashboard/.test(window.location) ? 97 : 167)
          }).control(CMS.Controllers.ResizeWidgets);

    }
    $(".column-set[id][data-resize]").each(bindResizer);//get anything that exists on the page already.

    //Then listen for new ones
    $(document.body).on("mouseover", ".column-set[id][data-resize]:not(.cms_controllers_resize_widgets)", bindResizer);

    var $area = $('.area').first()
      ;

    if (/\w+\/\d+($|\?|\#)/.test(window.location)) {
      $area.cms_controllers_page_object({
          model_descriptors: model_descriptors
        , instance: GGRC.make_model_instance(GGRC.page_object)
        });
    } else if (/dashboard/.test(window.location)) {
      $area.cms_controllers_dashboard({
          model_descriptors: model_descriptors
        , menu_tree_spec: dashboard_menu_spec
        , default_widgets: ['program']
        })
    } else if (/admin/.test(window.location)) {
      $area.cms_controllers_dashboard({
          model_descriptors: model_descriptors
        , menu_tree_spec: admin_menu_spec
      });
    } else {
      $area.cms_controllers_dashboard({ model_descriptors: [] });
    }

    /*$(".widget-add-placeholder").cms_controllers_add_widget({
        parent_controller : dashboard_controller
      , widget_descriptors : widget_descriptors
      , menu_tree : (/dashboard/.test(window.location) ? dashboard_menu : null)
      , minimum_widget_height : 100
    });*/

    /*function bindSortable(ev) {
        can.getObject("Instances", CMS.Controllers.SortableWidgets, true)[this.id] = 
         $(this)
          .cms_controllers_sortable_widgets({
            model : data[0]
          }).control(CMS.Controllers.SortableWidgets);
    }
    $(".widget-area").each(bindSortable);//get anything that exists on the page already.
    //we will need to consider whether to look for late-added ones later.
    */
  });


  $("body").on("click", ".note-trigger, .edit-notes", function(ev) {
    ev.stopPropagation();
    var $object = $(ev.target).closest("[data-object-id]")
    , type = $object.data("object-type")
    , notes_model = widget_descriptors[type].model
    , sec;

    $(ev.target).closest(".note").cms_controllers_section_notes({
      section_id : $object.data("object-id") || (/\d+$/.exec(window.location.pathname) || [null])[0]
      , model_class : notes_model
    });
  });

  $("section[id$=_info_widget]:not([id$=_more_info_widget])").ggrc_controllers_info_widget();

});

})(this, jQuery);
