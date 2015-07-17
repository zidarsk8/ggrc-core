/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

//= require controllers/resize_widgets_controller
//= require controllers/dashboard_widgets
//= require models/simple_models
//= require controls/control
//= require sections/section
//= require pbc/system

(function(namespace, $) {

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
    , object_display : "People"
    , tooltip_view : "/static/mustache/people/object_tooltip.mustache"
    , header_view : "/static/mustache/people/filters.mustache"  // includes only the filter, not the column headers
    , list_view : "/static/mustache/people/object_list.mustache"
    , fetch_post_process : sort_by_name_email
  }
  , "roles" : {
      model : CMS.Models.Role
    , extra_params : { scope__in: "System,Admin,Private Program,Workflow" }
    , object_category : "governance"
    , object_display : "Roles"
    , list_view : "/static/mustache/roles/object_list.mustache"
    , fetch_post_process : sort_by_name_email
  }
  , "events" : {
      model : CMS.Models.Event
    , object_category : "governance"
    , object_display : "Events"
    , list_view : "/static/mustache/events/object_list.mustache"
  }
  , "custom_attributes" : {
    parent_instance: CMS.Models.CustomAttributable,
    model: CMS.Models.CustomAttributable,
    show_view: GGRC.mustache_path + "/custom_attribute_definitions/tree.mustache",
    sortable: false,
    list_loader: function(instance) {
      return instance.findAll();
    },
    draw_children: true,
    child_options: [{
      model: CMS.Models.CustomAttributeDefinition,
      mapping: "custom_attribute_definitions",
      show_view: GGRC.mustache_path + "/custom_attribute_definitions/subtree.mustache",
      footer_view: null,
      add_item_view: null
    }]
  }
};


$(function() {
var admin_widgets = new GGRC.WidgetList("ggrc_admin", {
  admin : {
    "people" : {
        "model" : CMS.Models.Person
      , "content_controller": GGRC.Controllers.ListView
      , "content_controller_options": admin_list_descriptors["people"]
      , "widget_id" : "people_list"
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
      , "widget_icon" : "event"
      , widget_name: function() {
        return "Events";
      }
      , widget_info : function() {
        return "";
      }
    }
    , custom_attributes : {
      widget_id: "custom_attribute",
      widget_name: "Custom Attributes",
      widget_icon: "workflow",
      content_controller: CMS.Controllers.TreeView,
      content_controller_selector: "ul",
      model: CMS.Models.CustomAttributable,
      widget_initial_content: '<ul class="tree-structure new-tree colored-list" data-no-pin="true"></ul>',
      content_controller_options: admin_list_descriptors["custom_attributes"]
    }
  }
});


    var $area = $('.area').first(), instance, model_name,
        extra_page_options, defaults, object_browser;


    extra_page_options = {
        Program: {
            header_view: GGRC.mustache_path + "/base_objects/page_header.mustache"
          , page_title: function(controller) {
              return "GRC Program: " + controller.options.instance.title;
            }

        }
      , Person: {
            header_view: GGRC.mustache_path + "/base_objects/page_header.mustache"
          , page_title: function(controller) {
              var instance = controller.options.instance;
              return /dashboard/.test(window.location)
                ? "GRC: My Work"
                : "GRC Profile: " + (instance.name && instance.name.trim()) || (instance.email && instance.email.trim());
            }

        }
    };

    object_browser = /^\/objectBrowser\/?$/.test(window.location.pathname);

    if (/^\/\w+\/\d+($|\?|\#)/.test(window.location.pathname) || /^\/dashboard/.test(window.location.pathname)
        || object_browser) {
    //if (/\w+\/\d+($|\?|\#)/.test(window.location) || /dashboard/.test(window.location)) {
      instance = GGRC.page_instance();
      model_name = instance.constructor.shortName;

      // Ensure each extension has had a chance to initialize widgets
      can.each(GGRC.extensions, function(extension) {
        if (extension.init_widgets)
          extension.init_widgets();
      });
      defaults = Object.keys(GGRC.WidgetList.get_widget_list_for(model_name));

      //Remove info and task tabs from object-browser list of tabs
      if (object_browser) {
        defaults.splice(defaults.indexOf('info'), 1);
        defaults.splice(defaults.indexOf('task'), 1);
      }

      $area.cms_controllers_page_object($.extend({
        //model_descriptors: model_descriptors,
        widget_descriptors: GGRC.WidgetList.get_widget_list_for(model_name)
        , default_widgets: defaults || GGRC.default_widgets || []
        , instance: GGRC.page_instance()
        , header_view: GGRC.mustache_path + "/base_objects/page_header.mustache"
        , page_title: function(controller) {
            return controller.options.instance.title;
          }
        , page_help: function(controller) {
            return controller.options.instance.constructor.table_singular;
          }
        , current_user: GGRC.current_user
        }, extra_page_options[model_name]));
    } else if (/^\/admin\/?$/.test(window.location.pathname)) {

      $area.cms_controllers_dashboard({
          widget_descriptors: GGRC.WidgetList.get_widget_list_for("admin")
        , menu_tree_spec: GGRC.admin_menu_spec
        , default_widgets : ["people", "roles", "events", "custom_attributes"]
      });

      // Ensure each extension has had a chance to initialize admin widgets
      can.each(GGRC.extensions, function(extension) {
        if (extension.init_admin_widgets)
          extension.init_admin_widgets();
      });

    } else {
      $area.cms_controllers_dashboard({
        widget_descriptors: GGRC.widget_descriptors,
        default_widgets : GGRC.default_widgets
      });
    }

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
