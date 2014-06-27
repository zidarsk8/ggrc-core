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

    attributes: {
      workflow: "CMS.Models.Workflow.stub",
      task_group_tasks: "CMS.Models.TaskGroupTask.stubs",
      tasks: "CMS.Models.Task.stubs",
      task_group_objects: "CMS.Models.TaskGroupObject.stubs",
      objects: "CMS.Models.get_stubs",
      modified_by: "CMS.Models.Person.stub",
      context: "CMS.Models.Context.stub"
    },

    tree_view_options: {
      //show_view: GGRC.mustache_path + "/task_groups/tree.mustache",
      footer_view: GGRC.mustache_path + "/task_groups/tree_footer.mustache"
    },

    init: function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
      this.validatePresenceOf("end_date");
      this.validate(["_transient.contact", "contact"], function(newVal, prop) {
        var contact = this.attr("contact");
        var contact_text = this.attr("_transient.contact");
        if(
          !contact
          || !contact_text
          || (contact_text && !contact)
          || (contact_text !== "" && contact_text != null && contact != null && contact_text !== contact.reify().email)) {
          return "No valid contact selected for assignee";
        }
      });
    }
  }, {});

})(window.can);
