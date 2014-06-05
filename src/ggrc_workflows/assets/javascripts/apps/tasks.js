/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: sasmita
 * Maintained By: 
 */


(function($, CMS, GGRC) {

  var TaskExtension = {},
    _task_object_types = [];

  // Register `task` extension with GGRC
  GGRC.extensions.push(TaskExtension);

  TaskExtension.name = "tasks";

  // Register Task models for use with `infer_object_type`
  TaskExtension.object_type_decision_tree = function() {
    return {
      "task": CMS.Models.Task,
    };
  };

  // Configure mapping extensions for ggrc_workflows
  TaskExtension.init_mappings = function init_mappings(){
  };
  
  // Override GGRC.extra_widget_descriptors and GGRC.extra_default_widgets
  // Initialize widgets for task page
  TaskExtension.init_widgets = function init_widgets() {
    var page_instance = GGRC.page_instance();

    if (page_instance instanceof CMS.Models.Task) {
      TaskExtension.init_widgets_for_task_page();
    } else {
      TaskExtension.init_widgets_for_other_pages();
    }
  };

  TaskExtension.init_widgets_for_other_pages =
      function init_widgets_for_other_pages() {
    var descriptor = {},
      page_instance = GGRC.page_instance();

    if(page_instance && ~can.inArray(page_instance.constructor.shortName, _task_object_types)) {
      descriptor[page_instance.constructor.shortName] = {
        task : {
          widget_id : "task",
          widget_name : "Tasks",
          content_controller : GGRC.Controllers.TreeView,
          content_controller_options : {
            mapping : "tasks",
            parent_instance : page_instance,
            model : CMS.Models.Task,
            show_view : GGRC.mustache_path + "/base_objects/tree.mustache",
            footer_view : GGRC.mustache_path + "/base_objects/tree_footer.mustache"
          }
        }
      };
    }
    new GGRC.WidgetList("ggrc_tasks", descriptor);
  };
  
  TaskExtension.init_widgets_for_task_page =
      function init_widgets_for_task_page() {
    var task_widget_descriptors = {},
        new_default_widgets = [
          "info"
        ],
        object = GGRC.page_instance(),
        object_descriptors = {};

    can.each(GGRC.WidgetList.get_current_page_widgets(), function(descriptor, name) {
      if (~new_default_widgets.indexOf(name))
        task_widget_descriptors[name] = descriptor;
    });

    $.extend(
      true,
      task_widget_descriptors,
      { info : {
        content_controller : GGRC.Controllers.InfoWidget,
        content_controller_options :
          { widget_view : GGRC.mustache_path + "/tasks/info.mustache" }
      }}
    );//<!-- /$.extend -->   
    new GGRC.WidgetList("ggrc_tasks", { Task : task_widget_descriptors });    
  } // <!--init_widgets_for_task_page -->

  TaskExtension.init_mappings();  

})(this.can.$, this.CMS, this.GGRC);