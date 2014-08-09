/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/


(function(can) {

  can.Model.Cacheable("CMS.Models.TaskGroup", {
    root_object: "task_group",
    root_collection: "task_groups",
    category: "workflow",
    findAll: "GET /api/task_groups",
    findOne: "GET /api/task_groups/{id}",
    create: "POST /api/task_groups",
    update: "PUT /api/task_groups/{id}",
    destroy: "DELETE /api/task_groups/{id}",

    mixins: ["contactable"],

    attributes: {
      contact : "CMS.Models.Person.stub",
      workflow: "CMS.Models.Workflow.stub",
      task_group_tasks: "CMS.Models.TaskGroupTask.stubs",
      tasks: "CMS.Models.Task.stubs",
      task_group_objects: "CMS.Models.TaskGroupObject.stubs",
      objects: "CMS.Models.get_stubs",
      modified_by: "CMS.Models.Person.stub",
      context: "CMS.Models.Context.stub",
      end_date: "date",
    },

    tree_view_options: {
      sort_property: 'sort_index',
      //show_view: GGRC.mustache_path + "/task_groups/tree.mustache",
      footer_view: GGRC.mustache_path + "/task_groups/tree_footer.mustache"
    },

    init: function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
      this.validate(["_transient.contact", "contact"], function(newVal, prop) {
        var contact_exists = this.contact ? true : false;
        var reified_contact = contact_exists ? this.contact.reify() : false;
        var contact_has_email_address = reified_contact ? reified_contact.email : false;

        // This check will not work until the bug introduced with commit 8a5f600c65b7b45fd34bf8a7631961a6d5a19638
        // is resolved.
        if(!contact_has_email_address) {
          return "No valid contact selected for assignee";
        }
      });
    }
  }, {});


  can.Model.Cacheable("CMS.Models.TaskGroupTask", {
    root_object: "task_group_task",
    root_collection: "task_group_tasks",
    findAll: "GET /api/task_group_tasks",
    create: "POST /api/task_group_tasks",
    update: "PUT /api/task_group_tasks/{id}",
    destroy: "DELETE /api/task_group_tasks/{id}",

    mixins : ["contactable"],
    attributes: {
      context: "CMS.Models.Context.stub",
      contact: "CMS.Models.Person.stub",
      modified_by: "CMS.Models.Person.stub",
      task_group: "CMS.Models.TaskGroup.stub",
    },

    init: function() {
      var that = this;
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");

      this.bind("created", function(ev, instance) {
        if (instance instanceof that) {
          if (instance.task_group.reify().selfLink) {
            instance.task_group.reify().refresh();
          }
        }
      });
    }
  }, {
  });


})(window.can);
