/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/


(function(can) {

  var _mustache_path,
      overdue_compute,
      refresh_attr,
      refresh_attr_wrap;

  overdue_compute = can.compute(function(val) {
    if (this.attr("status") === "Verified") {
      return "";
    }
    var date = moment(this.attr("end_date"));
    if(date && date.isBefore(new Date())){
      return "overdue";
    }
    return "";
  });

  refresh_attr = function(instance, attr){
    if (instance.attr(attr).reify().selfLink) {
      instance.attr(attr).reify().refresh();
    }
  };

  refresh_attr_wrap = function(attr){
    return function(ev, instance) {
      if (instance instanceof this) {
        refresh_attr(instance, attr);
      }
    };
  };

  _mustache_path = GGRC.mustache_path + "/cycles";
  can.Model.Cacheable("CMS.Models.Cycle", {
    root_object: "cycle",
    root_collection: "cycles",
    category: "workflow",
    findAll: "GET /api/cycles",
    findOne: "GET /api/cycles/{id}",
    create: "POST /api/cycles",
    update: "PUT /api/cycles/{id}",
    destroy: "DELETE /api/cycles/{id}",

    attributes: {
      workflow: "CMS.Models.Workflow.stub",
      cycle_task_groups: "CMS.Models.CycleTaskGroup.stubs",
      modified_by: "CMS.Models.Person.stub",
      context: "CMS.Models.Context.stub"
    },

    tree_view_options: {
      show_view: _mustache_path + "/tree.mustache",
      //footer_view: _mustache_path + "/tree_footer.mustache",
      draw_children: true,
      child_options: [
        {
          model: "CycleTaskGroup",
          mapping: "cycle_task_groups",
          allow_creating: false
        }
      ]
    },
    init: function(){
      var that = this;
      this._super.apply(this, arguments);
      this.bind("created", refresh_attr_wrap('workflow').bind(this));
    }
  }, {
    init: function() {
      this._super.apply(this, arguments);
      this.bind("status", function(ev, newVal) {
        if(newVal === 'Verified' && this.workflow.reify().object_approval) {
          this.attr("is_current", false);
        }
      });
    }
  });

  _mustache_path = GGRC.mustache_path + "/cycle_task_entries";
  can.Model.Cacheable("CMS.Models.CycleTaskEntry", {
    root_object: "cycle_task_entry",
    root_collection: "cycle_task_entries",
    category: "workflow",
    findAll: "GET /api/cycle_task_entries",
    findOne: "GET /api/cycle_task_entries/{id}",
    create: "POST /api/cycle_task_entries",
    update: "PUT /api/cycle_task_entries/{id}",
    destroy: "DELETE /api/cycle_task_entries/{id}",

    attributes: {
      cycle_task_group_object_task: "CMS.Models.CycleTaskGroupObjectTask.stub",
      modified_by: "CMS.Models.Person.stub",
      context: "CMS.Models.Context.stub",
      object_documents: "CMS.Models.ObjectDocument.stubs",
      documents: "CMS.Models.Document.stubs",
      cycle: "CMS.Models.Cycle.stub",
    },

    tree_view_options: {
      show_view: _mustache_path + "/tree.mustache",
      footer_view: _mustache_path + "/tree_footer.mustache",
      child_options: [{
        //0: Documents
        model: "Document",
        mapping: "documents",
        show_view: _mustache_path + "/documents.mustache",
        footer_view: _mustache_path + "/documents_footer.mustache"
      }],
    },
    init: function(){
      this._super.apply(this, arguments);
      this.bind("created",
        refresh_attr_wrap("cycle_task_group_object_task").bind(this));
      this.validatePresenceOf("description");
    }
  }, {
    workflowFolder: function() {
      return this.refresh_all('cycle', 'workflow', 'folders').then(function(folders){
        if (folders.length === 0) {
          // Workflow folder has not been assigned
          return null;
        }
        return folders[0].instance;
      });
    }
  });


  _mustache_path = GGRC.mustache_path + "/cycle_task_groups";
  can.Model.Cacheable("CMS.Models.CycleTaskGroup", {
    root_object: "cycle_task_group",
    root_collection: "cycle_task_groups",
    category: "workflow",
    findAll: "GET /api/cycle_task_groups",
    findOne: "GET /api/cycle_task_groups/{id}",
    create: "POST /api/cycle_task_groups",
    update: "PUT /api/cycle_task_groups/{id}",
    destroy: "DELETE /api/cycle_task_groups/{id}",

    attributes: {
      cycle: "CMS.Models.Cycle.stub",
      task_group: "CMS.Models.TaskGroup.stub",
      cycle_task_group_objects: "CMS.Models.CycleTaskGroupObject.stubs",
      modified_by: "CMS.Models.Person.stub",
      context: "CMS.Models.Context.stub"
    },

    tree_view_options: {
      sort_property: 'sort_index',
      show_view: _mustache_path + "/tree.mustache",
      //footer_view: _mustache_path + "/tree_footer.mustache",
      draw_children: true,
      child_options: [
        {
          model: "CycleTaskGroupObject",
          mapping: "cycle_task_group_objects",
          allow_creating: false
        }
      ]
    }
  }, {
    overdue: overdue_compute,
  });


  _mustache_path = GGRC.mustache_path + "/cycle_task_group_objects";
  can.Model.Cacheable("CMS.Models.CycleTaskGroupObject", {
    root_object: "cycle_task_group_object",
    root_collection: "cycle_task_group_objects",
    category: "workflow",
    findAll: "GET /api/cycle_task_group_objects",
    findOne: "GET /api/cycle_task_group_objects/{id}",
    create: "POST /api/cycle_task_group_objects",
    update: "PUT /api/cycle_task_group_objects/{id}",
    destroy: "DELETE /api/cycle_task_group_objects/{id}",

    attributes: {
      cycle_task_group: "CMS.Models.CycleTaskGroup.stub",
      task_group_object: "CMS.Models.TaskGroupObject.stub",
      cycle_task_group_object_tasks:
        "CMS.Models.CycleTaskGroupObjectTask.stubs",
      modified_by: "CMS.Models.Person.stub",
      context: "CMS.Models.Context.stub",
      cycle: "CMS.Models.Cycle.stub",
      object: "CMS.Models.get_stub",
    },

    tree_view_options: {
      show_view: _mustache_path + "/tree.mustache",
      //footer_view: _mustache_path + "/tree_footer.mustache",
      draw_children: true,
      child_options: [
        {
          model: "CycleTaskGroupObjectTask",
          mapping: "cycle_task_group_object_tasks",
          allow_creating: false
        }
      ]
    },

    init: function() {
      this._super.apply(this, arguments);
      this.bind("updated", refresh_attr_wrap("cycle_task_group").bind(this));
    }
  }, {
    overdue: overdue_compute
  });


  _mustache_path = GGRC.mustache_path + "/cycle_task_group_object_tasks";
  can.Model.Cacheable("CMS.Models.CycleTaskGroupObjectTask", {
    root_object: "cycle_task_group_object_task",
    root_collection: "cycle_task_group_object_tasks",
    category: "workflow",
    findAll: "GET /api/cycle_task_group_object_tasks",
    findOne: "GET /api/cycle_task_group_object_tasks/{id}",
    create: "POST /api/cycle_task_group_object_tasks",
    update: "PUT /api/cycle_task_group_object_tasks/{id}",
    destroy: "DELETE /api/cycle_task_group_object_tasks/{id}",

    attributes: {
      cycle_task_group_object: "CMS.Models.CycleTaskGroupObject.stub",
      task_group_task: "CMS.Models.TaskGroupTask.stub",
      cycle_task_entries: "CMS.Models.CycleTaskEntry.stubs",
      modified_by: "CMS.Models.Person.stub",
      contact: "CMS.Models.Person.stub",
      context: "CMS.Models.Context.stub",
      cycle: "CMS.Models.Cycle.stub",
    },

    tree_view_options: {
      sort_property: 'sort_index',
      show_view: _mustache_path + "/tree.mustache",
      draw_children: true,
      child_options: [
        {
          model: "CycleTaskEntry",
          mapping: "cycle_task_entries",
          allow_creating: true
        }
      ]
    },

    init: function() {
      var that = this;
      this._super.apply(this, arguments);

      this.bind("updated", function(ev, instance) {
        if (instance instanceof that) {
          var object = instance.cycle_task_group_object.reify(),
              dfd = object.refresh(),
              rq = new RefreshQueue();

          function force_refresh_chain(chain) {
            can.reduce(chain, function(a, b) {
              return a.then(function(obj) {
                  return obj[b].reify().refresh();
              });
            }, dfd);
          }
          force_refresh_chain(["cycle_task_group", "cycle", "workflow"]);
          force_refresh_chain(["task_group_object", "object"]);
        }
      });
    }
  }, {
    overdue: overdue_compute,
    workflow: function() {
      return this.refresh_all('cycle', 'workflow').then(function(workflow){
        return workflow;
      });
    },
    object: function() {
      return this.refresh_all('cycle_task_group_object', 'task_group_object', 'object').then(function(object){
        return object;
      });
    }
  });

})(window.can);
