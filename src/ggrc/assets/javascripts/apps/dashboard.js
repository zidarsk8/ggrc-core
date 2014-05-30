/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
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
  , "standard" : {
    model : CMS.Models.Standard
    , object_type : "standard"
    , object_category : "governance"
    , object_route : "directives"
    , object_display : "Standards"
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
  , "system_or_process" : {
    model : CMS.Models.SystemOrProcess
    , object_type : "system_or_process"
    , object_category : "business"
    , object_route : "systems_or_processes"
    , object_display : "Systems or Processes"
  }
  , "system" : {
    model : CMS.Models.System
    , object_type : "system"
    , object_category : "business"
    , object_route : "systems"
    , object_display : "Systems"
  }
  , "process" : {
    model : CMS.Models.Process
    , object_type : "process"
    , object_category : "business"
    , object_route : "processes"
    , object_display : "Processes"
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
    model : CMS.Models.SystemOrProcess
    , object_type : "system_process"
    , object_category : "business"
    , object_route : "systems_or_processes"
    , object_display : "Systems/Processes"
    , widget_view : "/static/mustache/systems/object_widget.mustache"
  }
  , "system" : {
    model : CMS.Models.System
    , object_type : "system"
    , object_category : "business"
    , object_route : "systems"
    , object_display : "Systems"
  }
  , "sectionslug" : {
    model : CMS.Models.Section
    , object_type : "section"
    , object_route : "sections"
    , object_category : "governance"
  }
  , "audit" : {
    model : CMS.Models.Audit
    , object_type : "audit"
    , object_route : "audits"
    , object_category : "programs"
  }
  , "person" : {
    model : CMS.Models.Person
    , object_type : "person"
    , object_route : "people"
    , object_category : "entities"
  }
  , "org_group" : {
    model : CMS.Models.OrgGroup
    , object_type : "org_group"
    , object_category : "entities"
    , object_route : "org_groups"
    , object_display : "Org Groups"
  }
  , "document" : {
    model : CMS.Models.Document
    , object_type : "document"
    , object_route : "documents"
    , object_category : "business"
  }
};

var sort_by_name_email = function(list) {
  return new list.constructor(can.makeArray(list).sort(function(a,b) {
    a = a.person || a;
    b = b.person || b;
    a = (can.trim(a.name) || can.trim(a.email)).toLowerCase();
    b = (can.trim(b.name) || can.trim(b.email)).toLowerCase();
    if (a > b) return 1;
    if (a < b) return -1;
    return 0;
  }));
};

var admin_list_descriptors = {
  "people" : {
      model : CMS.Models.Person
    , roles: new can.Observe.List()
    , init : function() {
        var self = this;
        CMS.Models.Role.findAll({ scope__in: "System,Admin" }).done(function(roles) {
          self.roles.replace(sort_by_name_email(roles));
        });
      }
    , object_type : "person"
    , object_category : "governance"
    , object_route : "people"
    , object_display : "People"
    , tooltip_view : "/static/mustache/people/object_tooltip.mustache"
    , header_view : "/static/mustache/people/filters.mustache"
    , list_view : "/static/mustache/people/object_list.mustache"
    , fetch_post_process : sort_by_name_email
  }
  , "roles" : {
      model : CMS.Models.Role
    , extra_params : { scope__in: "System,Admin,Private Program" }
    , object_type : "role"
    , object_category : "governance"
    , object_route : "roles"
    , object_display : "Roles"
    , list_view : "/static/mustache/roles/object_list.mustache"
    , fetch_post_process : sort_by_name_email
  }
  , "events" : {
      model : CMS.Models.Event
    , object_type : "event"
    , object_category : "governance"
    , object_route : "events"
    , object_display : "Events"
    , list_view : "/static/mustache/events/object_list.mustache"
  }
};

GGRC.admin_widget_descriptors = {
  "people" : {
      "model" : CMS.Models.Person
    , "content_controller": GGRC.Controllers.ListView
    , "content_controller_options": admin_list_descriptors["people"]
    , "widget_id" : "people_list"
    , "widget_name" : "People"
    , "widget_icon" : "person"
    , "show_filter" : false
    , widget_name: function() {
      return "People";
    }
    , widget_info : function() {
      return "";
    }
  }
  , "roles" : {
      "model" : CMS.Models.Role
    , "content_controller": GGRC.Controllers.ListView
    , "content_controller_options": admin_list_descriptors["roles"]
    , "widget_id" : "roles_list"
    , "widget_name" : "Roles"
    , "widget_icon" : "role"
    , "show_filter" : false
    , widget_name: function() {
      return "Roles";
    }
    , widget_info : function() {
      return "";
    }
  }
  , "events" : {
      "model" : CMS.Models.Event
    , "content_controller": GGRC.Controllers.ListView
    , "content_controller_options": admin_list_descriptors["events"]
    , "widget_id" : "events_list"
    , "widget_name" : "Events"
    , "widget_icon" : "event"
    , widget_name: function() {
      return "Events";
    }
    , widget_info : function() {
      return "";
    }
  }
};

if (/admin\/\d+/.test(window.location)) {
  var widget_ids = [];

  if (!GGRC.extra_widget_descriptors)
    GGRC.extra_widget_descriptors = {};
  $.extend(GGRC.extra_widget_descriptors, program_widget_descriptors);

  if (!GGRC.extra_default_widgets)
    GGRC.extra_default_widgets = [];
  GGRC.extra_default_widgets.push.apply(
      GGRC.extra_default_widgets, widget_ids);
}



dashboard_menu_spec = [
  { title : "Governance / Compliance"
  , objects: [ "regulation", "policy", "standard", "contract", "control" ]
  },
  { title : "Asset / Business"
  , objects: [ "system", "process", "project"
             , "facility", "product", "data_asset", "market" ]
  },
  { title : "People / Groups"
  , objects: [ "people", "org_group" ]
  },
  /*{ title : "Risk"
  , objects: [ "risky_attributes", "risk" ]
  }*/
]

//function make_admin_menu(widget_descriptors) {
GGRC.admin_menu_spec = [
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
            //, minimum_widget_height : (/dashboard/.test(window.location) ? 97 : 167)
          }).control(CMS.Controllers.ResizeWidgets);

    }
    //$(".column-set[id][data-resize]").each(bindResizer);//get anything that exists on the page already.

    //Then listen for new ones
    //$(document.body).on("mouseover", ".column-set[id][data-resize]:not(.cms_controllers_resize_widgets)", bindResizer);

    var $area = $('.area').first()
      , instance
      , model_name
      , extra_page_options
      ;

    extra_page_options = {
        Program: {
            header_view: GGRC.mustache_path + "/programs/page_header.mustache"
          , page_title: function(controller) {
              return "GRC Program: " + controller.options.instance.title;
            }

        }
      , Person: {
            header_view: GGRC.mustache_path + "/people/page_header.mustache"
          , page_title: function(controller) {
              var instance = controller.options.instance;
              return /dashboard/.test(window.location)
                ? "GRC: My Work"
                : "GRC Profile: " + (instance.name && instance.name.trim()) || (instance.email && instance.email.trim());
            }

        }
    };

    if (/^\/\w+\/\d+($|\?|\#)/.test(window.location.pathname) || /^\/dashboard/.test(window.location.pathname)) {
    //if (/\w+\/\d+($|\?|\#)/.test(window.location) || /dashboard/.test(window.location)) {
      instance = GGRC.page_instance();
      model_name = instance.constructor.shortName;

      // Ensure each extension has had a chance to initialize widgets
      can.each(GGRC.extensions, function(extension) {
        if (extension.init_widgets)
          extension.init_widgets();
      });

      $area.cms_controllers_page_object($.extend({
          model_descriptors: model_descriptors
        , widget_descriptors: GGRC.extra_widget_descriptors || {}
        , default_widgets: GGRC.extra_default_widgets || []
        , instance: GGRC.page_instance()
        , header_view: GGRC.mustache_path + "/base_objects/page_header.mustache"
        , page_title: function(controller) {
            return controller.options.instance.title;
          }
        , page_help: function(controller) {
            return controller.options.instance.constructor.table_singular;
          }
        }, extra_page_options[model_name]));
    } else if (/^\/admin\/?$/.test(window.location.pathname)) {
      $area.cms_controllers_dashboard({
          widget_descriptors: GGRC.admin_widget_descriptors
        , menu_tree_spec: GGRC.admin_menu_spec
        , default_widgets : ["people", "roles", "events"]
      });
    } else {
      $area.cms_controllers_dashboard({ model_descriptors: [] });
    }

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
});

})(this, jQuery);
