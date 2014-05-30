/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: dan@reciprocitylabs.com
 * Maintained By: dan@reciprocitylabs.com
 */


(function($, CMS, GGRC) {
  var WorkflowExtension = {};

  // Register `workflows` extension with GGRC
  GGRC.extensions.push(WorkflowExtension);

  WorkflowExtension.name = "workflows";

  // Register Workflow models for use with `infer_object_type`
  WorkflowExtension.object_type_decision_tree = function() {
    return {
      "workflow": CMS.Models.Workflow,
      "task": CMS.Models.Task,
      "task_group": CMS.Models.TaskGroup
    };
  };

  // Configure mapping extensions for ggrc_workflows
  WorkflowExtension.init_mappings = function init_mappings() {
    var Proxy = GGRC.MapperHelpers.Proxy,
        Direct = GGRC.MapperHelpers.Direct,
        Cross = GGRC.MapperHelpers.Cross,
        CustomFilter = GGRC.MapperHelpers.CustomFilter;

    // Add mappings for basic workflow objects
    $.extend(GGRC.Mappings,
      {
        Task: {
          subtasks: Direct(
            "CycleTask", "task", "tasks")
        },

        Cycle: {
          tasks: Direct(
            "CycleTask", "cycle", "tasks")
        },

        Workflow: {
          objects: Proxy(
            null, "object", "WorkflowObject", "workflow", "workflow_objects"),
          tasks: Proxy(
            "Task", "task", "WorkflowTask", "workflow", "workflow_tasks"),
          people: Proxy(
            "Person", "person", "WorkflowPerson", "workflow", "workflow_people"),
          task_groups: Direct(
            "TaskGroup", "workflow", "task_groups"),
          cycles: Direct(
            "Cycle", "workflow", "cycles"),
          previous_cycles: CustomFilter("cycles", function(result) {
              return result.instance.status == "Finished";
            }),
          current_cycle: CustomFilter("cycles", function(result) {
              return result.instance.status != "Finished";
            }),
          current_tasks: Cross("current_cycle", "tasks")
        }
      });

    // Insert `workflows` mappings to all business object types
    var _workflow_object_types = [
      "Program",
      "Regulation", "Standard", "Policy", "Contract",
      "Objective", "Control", "Section", "Clause",
      "System", "Process",
      "DataAsset", "Facility", "Market", "Product", "Project"
      ];

    can.each(_workflow_object_types, function(type) {
      GGRC.Mappings[type].workflows = new GGRC.ListLoaders.ProxyListLoader(
        "WorkflowObject", "object", "workflow", "workflow_objects", null);
    });
  };

  // Construct and add JoinDescriptors for workflow extension
  WorkflowExtension.init_join_descriptors = function init_join_descriptors() {
    var join_descriptor_arguments = [
      [all_object_types, "Workflow", "WorkflowObject", "workflow", "object"],
      ["Workflow", all_object_types, "WorkflowObject", "object", "workflow"],
      ["Workflow", "Task", "WorkflowTask", "task", "workflow"],
      ["Task", "Workflow", "WorkflowTask", "workflow", "task"],
      ["Workflow", "TaskGroup", null, null, "workflow"],
      //["Workflow", "TaskGroup", "TaskGroup", "task_group", "workflow"],
      //["TaskGroup", "Workflow", "TaskGroup", "workflow", "task_group"],
      ["Workflow", "Person", "WorkflowPerson", "person", "workflow"],
      ["Person", "Workflow", "WorkflowPerson", "workflow", "person"],
      [all_object_types, "TaskGroup", "TaskGroupObject", "task_group", "object"],
      ["TaskGroup", all_object_types, "TaskGroupObject", "object", "task_group"],
      ["TaskGroup", "Task", "TaskGroupTask", "task", "task_group"],
      ["Task", "TaskGroup", "TaskGroupTask", "task_group", "task"]
    ];

    GGRC.JoinDescriptor.from_arguments_list(join_descriptor_arguments);
  };

  // Override GGRC.extra_widget_descriptors and GGRC.extra_default_widgets
  // Initialize widgets for workflow page
  WorkflowExtension.init_widgets = function init_widgets() {
    var page_instance = GGRC.page_instance();

    if (page_instance instanceof CMS.Models.Workflow) {
      WorkflowExtension.init_widgets_for_workflow_page();
    } else {
      WorkflowExtension.init_widgets_for_other_pages();
    }
  }

  WorkflowExtension.init_widgets_for_other_pages =
      function init_widgets_for_other_pages() {
    var index;

    // Explicitly remove `task_group` widget on other pages
    if (GGRC.extra_widget_descriptors.task_group)
      delete GGRC.extra_widget_descriptors.task_group;

    index = GGRC.extra_default_widgets.indexOf("task_group");
    if (index > -1)
      GGRC.extra_default_widgets.splice(index, 1);

    if (GGRC.extra_widget_descriptors.workflow) {
      GGRC.extra_widget_descriptors.workflow.content_controller_options.mapping =
        "workflows";
    }

    /*can.each(GGRC.extra_widget_descriptors, function(descriptor, name) {
      if (~new_default_widgets.indexOf(name))
        new_widget_descriptors[name] = descriptor;
    });*/
  };

  WorkflowExtension.init_widgets_for_workflow_page =
      function init_widgets_for_workflow_page() {
    var new_widget_descriptors = {},
        new_default_widgets = [
          "info",
          "objects", "task", "person", "task_group",
          "history", "current"
        ],
        objects_widget_descriptor,
        history_widget_descriptor,
        current_widget_descriptor,
        object = GGRC.page_instance();

    can.each(GGRC.extra_widget_descriptors, function(descriptor, name) {
      if (~new_default_widgets.indexOf(name))
        new_widget_descriptors[name] = descriptor;
    });

    new_widget_descriptors.info.content_controller_options.widget_view =
      GGRC.mustache_path + "/workflows/info.mustache";

    new_widget_descriptors.task.content_controller_options.mapping = "tasks";
    new_widget_descriptors.person.content_controller_options.mapping = "people";
    new_widget_descriptors.task_group.content_controller_options.mapping = "task_groups";

    objects_widget_descriptor = {
      content_controller: CMS.Controllers.TreeView,
      content_controller_selector: "ul",
      widget_initial_content: '<ul class="tree-structure new-tree"></ul>',
      widget_id: "objects",
      widget_name: "Objects",
      widget_icon: "object",
      //object_category: "objects",
      //model: can.Model.Cacheable //far_model,
      content_controller_options: {
        child_options: [],
        draw_children: false,
        parent_instance: object,
        model: can.Model.Cacheable,
        mapping: "objects",
        //show_view : GGRC.mustache_path + "/sections/tree.mustache",
        footer_view: GGRC.mustache_path + "/base_objects/tree_footer.mustache"
      }
    };
    history_widget_descriptor = {
      content_controller: CMS.Controllers.TreeView,
      content_controller_selector: "ul",
      widget_initial_content: '<ul class="tree-structure new-tree"></ul>',
      widget_id: "history",
      widget_name: "History",
      widget_icon: "history",
      //object_category: "history",
      //model: can.Model.Cacheable //far_model,
      content_controller_options: {
        child_options: [],
        draw_children: true,
        parent_instance: object,
        model: can.Model.Cacheable, //"Cycle"
        mapping: "previous_cycles",
        //show_view : GGRC.mustache_path + "/sections/tree.mustache",
        footer_view: GGRC.mustache_path + "/base_objects/tree_footer.mustache"
      }
    };
    current_widget_descriptor = {
      content_controller: CMS.Controllers.TreeView,
      content_controller_selector: "ul",
      widget_initial_content: '<ul class="tree-structure new-tree"></ul>',
      widget_id: "current",
      widget_name: "Current Cycle",
      widget_icon: "cycle",
      //object_category: "history",
      //model: can.Model.Cacheable //far_model,
      content_controller_options: {
        child_options: [],
        draw_children: true,
        parent_instance: object,
        model: can.Model.Cacheable, //"CycleTask"
        mapping: "current_tasks",
        //show_view : GGRC.mustache_path + "/sections/tree.mustache",
        footer_view: GGRC.mustache_path + "/base_objects/tree_footer.mustache"
      }
    };
    new_widget_descriptors.objects = objects_widget_descriptor;
    new_widget_descriptors.history = history_widget_descriptor;
    new_widget_descriptors.current = current_widget_descriptor;

    GGRC.extra_widget_descriptors = new_widget_descriptors;
    GGRC.extra_default_widgets = new_default_widgets;
  }


  GGRC.register_hook("LHN.Sections", GGRC.mustache_path + "/dashboard/lhn_workflows");

  WorkflowExtension.init_mappings();
  WorkflowExtension.init_join_descriptors();

})(this.can.$, this.CMS, this.GGRC);
