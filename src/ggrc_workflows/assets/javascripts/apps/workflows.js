/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: dan@reciprocitylabs.com
 * Maintained By: dan@reciprocitylabs.com
 */


(function($, CMS, GGRC) {
  var WorkflowExtension = {},
      _workflow_object_types = [
        "Program",
        "Regulation", "Standard", "Policy", "Contract",
        "Objective", "Control", "Section", "Clause",
        "System", "Process",
        "DataAsset", "Facility", "Market", "Product", "Project"
      ],
      _task_sort_function = function(a, b){
        var date_a = +new Date(a.end_date),
            date_b = +new Date(b.end_date);
        if(date_a === date_b){
          return a.id < b.id;
        }
        return date_a < date_b;
      };

  // Register `workflows` extension with GGRC
  GGRC.extensions.push(WorkflowExtension);

  WorkflowExtension.name = "workflows";

  // Register Workflow models for use with `infer_object_type`
  WorkflowExtension.object_type_decision_tree = function() {
    return {
      "cycle": CMS.Models.Cycle,
      "cycle_task_entry": CMS.Models.CycleTaskEntry,
      "cycle_task_group": CMS.Models.CycleTaskGroup,
      "cycle_task_group_object": CMS.Models.CycleTaskGroupObject,
      "cycle_task_group_object_task": CMS.Models.CycleTaskGroupObjectTask,

      "task": CMS.Models.Task,
      "task_group": CMS.Models.TaskGroup,
      "workflow": CMS.Models.Workflow
    };
  };

  // Configure mapping extensions for ggrc_workflows
  WorkflowExtension.init_mappings = function init_mappings() {
    var Proxy = GGRC.MapperHelpers.Proxy,
        Direct = GGRC.MapperHelpers.Direct,
        Cross = GGRC.MapperHelpers.Cross,
        Multi = GGRC.MapperHelpers.Multi,
        CustomFilter = GGRC.MapperHelpers.CustomFilter,
        Reify = GGRC.MapperHelpers.Reify,
        Search = GGRC.MapperHelpers.Search;

    // Add mappings for basic workflow objects
    var mappings = {
        Task: {
          _canonical: {
            subtasks: "Task",
            task_groups: "TaskGroup"
          },
          task_groups: Proxy(
            "TaskGroup", "task_group", "TaskGroupTask", "task", "task_group_tasks"),
        },

        TaskGroup: {
          _canonical: {
            tasks: "Task",
            objects: _workflow_object_types
          },
          task_group_tasks: Direct(
            "TaskGroupTask", "task_group", "task_group_tasks"),
          tasks: Proxy(
            "Task", "task", "TaskGroupTask", "task_group", "task_group_tasks"),
          objects: Proxy(
            null, "object", "TaskGroupObject", "task_group", "task_group_objects")
        },

        Workflow: {
          _canonical: {
            objects: _workflow_object_types.concat(["Cacheable"]),
            tasks: "Task",
            task_groups: "TaskGroup",
            people: "Person",
            folders: "GDriveFolder",
            context: "Context"
          },
          objects: Proxy(
            null, "object", "WorkflowObject", "workflow", "workflow_objects"),
          tasks: Proxy(
            "Task", "task", "WorkflowTask", "workflow", "workflow_tasks"),

          task_groups: Direct(
            "TaskGroup", "workflow", "task_groups"),
          cycles: Direct(
            "Cycle", "workflow", "cycles"),
          folders:
            new GGRC.ListLoaders.ProxyListLoader("ObjectFolder", "folderable", "folder", "object_folders", "GDriveFolder"),
          previous_cycles: CustomFilter("cycles", function(result) {
              return !result.instance.is_current;
            }),
          current_cycles: CustomFilter("cycles", function(result) {
              return result.instance.is_current;
            }),
          current_cycle: CustomFilter("cycles", function(result) {
              return result.instance.is_current;
            }),
          current_task_groups: Cross("current_cycle", "reify_cycle_task_groups"),
          current_task_group_objects: Cross("current_task_groups", "cycle_task_group_objects_for_page_object"),
          current_tasks: Cross("current_task_groups", "cycle_task_group_object_tasks_for_page_object"),

          people: Proxy(
            "Person", "person", "WorkflowPerson", "workflow", "workflow_people"),
          context: Direct(
            "Context", "related_object", "context"),
          authorization_contexts: Multi([
            "context"]), //, "contexts_via_audits"]),
          authorizations: Cross(
            "authorization_contexts", "user_roles"),
          authorized_people: Cross(
            "authorization_contexts", "authorized_people"),
          mapped_and_or_authorized_people: Multi([
            "people", "authorized_people"]),
          roles: Cross("authorizations", "role"),
          // This is a dummy mapping that ensures the WorkflowOwner role is loaded
          //  before we do the custom filter for owner_authorizations.
          authorizations_and_roles: Multi(["authorizations", "roles"]),
          owner_authorizations: CustomFilter("authorizations_and_roles", function(binding) {
            return binding.instance instanceof CMS.Models.UserRole
                   && binding.instance.role.reify().attr("name") === "WorkflowOwner";
          }),
          owners: Cross("owner_authorizations", "person")
        },

        Cycle: {
          cycle_task_groups: Direct(
            "CycleTaskGroup", "cycle", "cycle_task_groups"),
          reify_cycle_task_groups: Reify("cycle_task_groups")
        },

        CycleTaskGroup: {
          cycle: Direct(
            "Cycle", "cycle_task_groups", "cycle"),
          //task_group: Direct(
          //  "TaskGroup", "cycle", "tasks"),
          cycle_task_group_objects: Direct(
            "CycleTaskGroupObject",
            "cycle_task_group",
            "cycle_task_group_objects"),
          cycle_task_group_objects_for_page_object: CustomFilter(
            "cycle_task_group_objects", function(object) {
              return object.instance.task_group_object.reify().object.reify() === GGRC.page_instance();
            }),
          cycle_task_group_object_tasks_for_page_object: Cross(
            "cycle_task_group_objects_for_page_object", "cycle_task_group_object_tasks"
            )
        },

        CycleTaskGroupObject: {
          cycle: Direct(
            "Cycle", "cycle_task_group_objects", "cycle"),
          cycle_task_group: Direct(
            "CycleTaskGroup", "cycle_task_group_objects", "cycle_task_group"),
          task_group_object: Direct(
            "TaskGroupObject", "task_group_objects", "task_group_object"
          ),
          //task_group_object: Direct(
          //  "TaskGroupObject", "cycle", "tasks")
          cycle_task_group_object_tasks: Direct(
            "CycleTaskGroupObjectTask",
            "cycle_task_group_object",
            "cycle_task_group_object_tasks")
        },

        CycleTaskGroupObjectTask: {
          cycle: Direct(
            "Cycle", "cycle_task_group_object_tasks", "cycle"),
          cycle_task_group_object: Direct(
            "CycleTaskGroupObject",
            "cycle_task_group_object_tasks",
            "cycle_task_group_object"),
          //task_group_object: Direct(
          //  "TaskGroupObject", "cycle", "tasks")
          cycle_task_entries: Direct(
            "CycleTaskEntry",
            "cycle_task_group_object_task",
            "cycle_task_entries")
        },

        CycleTaskEntry: {
          documents: Proxy(
            "Document", "document", "ObjectDocument", "documentable", "object_documents"),
          cycle: Direct(
            "Cycle", "cycle_task_entries", "cycle"),
          cycle_task_group_object_task: Direct(
            "CycleTaskGroupObjectTask",
            "cycle_task_entries",
            "cycle_task_group_object_task")
        },

        People: {
          _canonical: {
            workflows: "Workflow",
          },
          workflows: Proxy(
            "Workflow", "workflow", "WorkflowPerson", "person", "workflow_people"),

        },
        Person: {
          assigned_tasks: Search(function(binding) {
            return CMS.Models.CycleTaskGroupObjectTask.findAll({
              contact_id: binding.instance.id,
              'cycle.is_current': true
            });
          })
        }
      };

    // Insert `workflows` mappings to all business object types
    can.each(_workflow_object_types, function(type) {
      mappings[type] = {};
      mappings[type].workflows = new GGRC.ListLoaders.ProxyListLoader(
        "WorkflowObject", "object", "workflow", "workflow_objects", null);
      mappings[type].approval_workflows = CustomFilter(
        "workflows", function(binding) {
          return binding.instance.object_approval;
        });
      mappings[type].task_groups = new GGRC.ListLoaders.ProxyListLoader(
        "TaskGroupObject", "object", "task_group", "task_group_objects", null);
      mappings[type].object_tasks = Search(function(binding) {
        return CMS.Models.CycleTaskGroupObjectTask.findAll({
          'cycle_task_group_object.object_id': binding.instance.id,
          'cycle_task_group_object.object_type': binding.instance.type,
          'cycle.is_current': true
        });
      });
      mappings[type]._canonical = {
       "workflows": "Workflow",
       "task_groups": "TaskGroup"
      };

      CMS.Models[type].attributes.workflow_objects =
        "CMS.Models.WorkflowObject.stubs";
      CMS.Models[type].attributes.task_group_objects =
        "CMS.Models.TaskGroupObject.stubs";

      // Also register a render hook for object approval
      GGRC.register_hook(
        type + ".info_widget_actions",
        GGRC.mustache_path + "/base_objects/approval_link.mustache"
        );

    });
    new GGRC.Mappings("ggrc_workflows", mappings);
  };

  // Override GGRC.extra_widget_descriptors and GGRC.extra_default_widgets
  // Initialize widgets for workflow page
  WorkflowExtension.init_widgets = function init_widgets() {
    var page_instance = GGRC.page_instance();

    if (page_instance instanceof CMS.Models.Workflow) {
      WorkflowExtension.init_widgets_for_workflow_page();
    } else if (page_instance instanceof CMS.Models.Task) {
      WorkflowExtension.init_widgets_for_task_page();
    } else if (page_instance instanceof CMS.Models.Person) {
      WorkflowExtension.init_widgets_for_person_page();
    } else {
      WorkflowExtension.init_widgets_for_other_pages();
    }
    WorkflowExtension.init_global();
  };

  WorkflowExtension.init_widgets_for_other_pages =
      function init_widgets_for_other_pages() {
    var descriptor = {},
        page_instance = GGRC.page_instance();

    if (page_instance && ~can.inArray(page_instance.constructor.shortName, _workflow_object_types)) {
      descriptor[page_instance.constructor.shortName] = {
        workflow: {
          widget_id: "workflow",
          widget_name: "Workflows",
          content_controller: GGRC.Controllers.TreeView,
          content_controller_options: {
            mapping: "workflows",
            parent_instance: page_instance,
            model: CMS.Models.Workflow,
            show_view: GGRC.mustache_path + "/workflows/tree.mustache",
            footer_view: GGRC.mustache_path + "/base_objects/tree_footer.mustache",
            draw_children: true,
            child_options: [{
              title_plural: "Current Tasks",
              model: CMS.Models.CycleTaskGroupObjectTask,
              mapping: "current_tasks",
              allow_creating: true,
              show_view: GGRC.mustache_path + "/cycle_task_group_object_tasks/tree.mustache",
              footer_view: GGRC.mustache_path + "/cycle_task_group_object_tasks/current_tg_tree_footer.mustache"
            }]
          }
        },
        task: {
          widget_id: 'task',
          widget_name: "Workflow Tasks",
          content_controller: GGRC.Controllers.TreeView,
          content_controller_options: {
            mapping: "object_tasks",
            parent_instance: page_instance,
            model: CMS.Models.CycleTaskGroupObjectTask,
            show_view: GGRC.mustache_path + "/cycle_task_group_object_tasks/tree.mustache",
            sort_property: null,
            sort_function: _task_sort_function,
            content_controller_options: {
              child_options: [
                {
                  model: can.Model.Cacheable,
                  mapping: "cycle_task_entries",
                  show_view: GGRC.mustache_path + "/cycle_task_entries/tree.mustache",
                  footer_view: GGRC.mustache_path + "/cycle_task_entries/tree_footer.mustache",
                  draw_children: true,
                  allow_creating: true
                },
              ]
            }
          }
        }
      };
    }
    new GGRC.WidgetList("ggrc_workflows", descriptor, [
      "info_widget",
      "task_widget"
    ]);
  };

  WorkflowExtension.init_widgets_for_task_page =
      function init_widgets_for_task_page() {

    var task_widget_descriptors = {},
        new_default_widgets = [
          "info"
        ];

    can.each(GGRC.WidgetList.get_current_page_widgets(), function(descriptor, name) {
      if (~new_default_widgets.indexOf(name))
        task_widget_descriptors[name] = descriptor;
    });

    $.extend(
      true,
      task_widget_descriptors,
      {
        info: {
          content_controller: GGRC.Controllers.InfoWidget,
          content_controller_options: {
            widget_view: GGRC.mustache_path + "/tasks/info.mustache"
          }
        }
      }
    );

    new GGRC.WidgetList("ggrc_workflows", { Task: task_widget_descriptors });
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
        object = GGRC.page_instance(),
        object_descriptors = {};

    can.each(GGRC.WidgetList.get_current_page_widgets(), function(descriptor, name) {
      if (~new_default_widgets.indexOf(name))
        new_widget_descriptors[name] = descriptor;
    });

    // Initialize controller -- probably this should go in a separate
    // initialization area
    $(function() {
      $(document.body).ggrc_controllers_workflow_page();
    });

    GGRC.register_hook(
        "ObjectNav.Actions",
        GGRC.mustache_path + "/dashboard/object_nav_actions");

    $.extend(
      true,
      new_widget_descriptors,
      {
        info: {
          content_controller: GGRC.Controllers.InfoWidget,
          content_controller_options: {
            widget_view: GGRC.mustache_path + "/workflows/info.mustache"
          }
        },
        task: {
          widget_id: "task",
          widget_name: "Tasks",
          widget_icon: "task",
          content_controller: GGRC.Controllers.TreeView,
          content_controller_options: {
            parent_instance: object,
            model: CMS.Models.Task,
            show_view: GGRC.mustache_path + "/tasks/tree.mustache",
            mapping: "tasks"
          }
        },
        person: {
          widget_id: "person",
          widget_name: "People",
          widget_icon: "person",
          content_controller: GGRC.Controllers.TreeView,
          content_controller_options: {
            parent_instance: object,
            model: CMS.Models.Person,
            mapping: "mapped_and_or_authorized_people",
            show_view: GGRC.mustache_path + "/ggrc_basic_permissions/people_roles/authorizations_by_person_tree.mustache",
            footer_view: GGRC.mustache_path + "/ggrc_basic_permissions/people_roles/authorizations_by_person_tree_footer.mustache",
            footer_view: GGRC.mustache_path + "/wf_people/tree_footer.mustache"
          }
        },
        task_group: {
          widget_id: "task_group",
          widget_name: "Task Groups",
          widget_icon: "task_group",
          content_controller: CMS.Controllers.SortableTreeView,
          content_controller_selector: "ul",
          widget_initial_content: '<ul class="tree-structure new-tree colored-list"></ul>',
          content_controller_options: {
            parent_instance: object,
            model: CMS.Models.TaskGroup,
            show_view: GGRC.mustache_path + "/task_groups/tree.mustache",
            mapping: "task_groups",
            draw_children: true,
            //note that we are using special naming for the tree views here.
            //  also, tasks for a task group aren't directly mapping to the
            //  tasks themselves but to the join object.  This is impotant
            //  since the join objects themselves have important attributes.
            child_options: [
              {
                model: can.Model.Cacheable,
                mapping: "objects",
                show_view: GGRC.mustache_path + "/base_objects/task_group_subtree.mustache",
                footer_view: GGRC.mustache_path + "/base_objects/task_group_subtree_footer.mustache"
              },
              {
                model: CMS.Models.Task,
                mapping: "task_group_tasks",
                show_view: GGRC.mustache_path + "/tasks/task_group_subtree.mustache",
                footer_view: GGRC.mustache_path + "/tasks/task_group_subtree_footer.mustache",
                sort_property: 'sort_index',
                allow_creating: true
              }
            ]
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
      //object_category: "objects",
      //model: can.Model.Cacheable //far_model,
      content_controller_options: {
        child_options: [],
        draw_children: false,
        parent_instance: object,
        model: can.Model.Cacheable,
        mapping: "objects",
        //show_view: GGRC.mustache_path + "/sections/tree.mustache",
        footer_view: GGRC.mustache_path + "/wf_objects/tree_footer.mustache"
      }
    };
    history_widget_descriptor = {
      content_controller: CMS.Controllers.TreeView,
      content_controller_selector: "ul",
      widget_initial_content: '<ul class="tree-structure new-tree colored-list"></ul>',
      widget_id: "history",
      widget_name: "History",
      widget_icon: "history",
      //object_category: "history",
      content_controller_options: {
        draw_children: true,
        parent_instance: object,
        model: "Cycle",
        mapping: "previous_cycles",
      }
    };
    current_widget_descriptor = {
      content_controller: CMS.Controllers.TreeView,
      content_controller_selector: "ul",
      widget_initial_content: '<ul class="tree-structure new-tree colored-list"></ul>',
      widget_id: "current",
      widget_name: "Current Cycle",
      widget_icon: "cycle",
      content_controller_options: {
        draw_children: true,
        parent_instance: object,
        model: "Cycle",
        mapping: "current_cycles",
      }
    };
    new_widget_descriptors.objects = objects_widget_descriptor;
    new_widget_descriptors.history = history_widget_descriptor;
    new_widget_descriptors.current = current_widget_descriptor;

    new GGRC.WidgetList("ggrc_workflows", { Workflow: new_widget_descriptors });

    // Setup extra refresh required due to automatic creation of permissions
    // on creation of WorkflowPerson
    CMS.Models.WorkflowPerson.bind("created", function(ev, instance) {
      if (instance instanceof CMS.Models.WorkflowPerson) {
        instance.context.reify().refresh();
      }
    });
  };

  WorkflowExtension.init_widgets_for_person_page =
      function init_widgets_for_person_page() {

    var descriptor = {},
        page_instance = GGRC.page_instance();

    descriptor[page_instance.constructor.shortName] = {
      task: {
        widget_id: 'task',
        widget_name: "My Tasks",
        content_controller: GGRC.Controllers.TreeView,

        content_controller_options: {
          parent_instance: GGRC.page_instance(),
          model: CMS.Models.CycleTaskGroupObjectTask,
          show_view: GGRC.mustache_path + "/cycle_task_group_object_tasks/tree.mustache",
          mapping: "assigned_tasks",
          draw_children: true,
          sort_property: null,
          sort_function: _task_sort_function,
          content_controller_options: {
            child_options: [
              {
                model: can.Model.Cacheable,
                mapping: "cycle_task_entries",
                show_view: GGRC.mustache_path + "/cycle_task_entries/tree.mustache",
                footer_view: GGRC.mustache_path + "/cycle_task_entries/tree_footer.mustache",
                draw_children: true,
                allow_creating: true
              },
            ]
          }
        }
      }
    };
    new GGRC.WidgetList("ggrc_workflows", descriptor, [
      "info_widget",
      "task_widget"
    ]);
  };

  WorkflowExtension.init_global = function() {
    $(function() {

      if(!GGRC.current_user || !GGRC.current_user.id){
        return;
      }
      CMS.Models.Person.findOne({
        id: GGRC.current_user.id
      }).then(function(person){
        $('.task-count').ggrc_controllers_mapping_count({
          mapping: 'assigned_tasks',
          instance: person
        });
      });
    });
  };

  GGRC.register_hook(
      "LHN.Sections_workflow", GGRC.mustache_path + "/dashboard/lhn_workflows");

  WorkflowExtension.init_mappings();

})(this.can.$, this.CMS, this.GGRC);
