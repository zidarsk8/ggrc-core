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
      context: "CMS.Models.Context.stub",
      end_date: "date",
    },

    tree_view_options: {
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
      // FIXME this should be done with a can.route (we can't currently do this without 
      //  being able to make arbitrary routes) and should not assume that there's a 
      //  task group widget.  We currently get away with this because there's only one
      //  place in the UI where Task Groups are created.  This is not a general solution
      //  to the problem and DO NOT COPY THIS CODE ELSEWHERE. --BM  7/16/2014
      this.bind("created", function(ev, data) {
        window.location.hash='task_group_widget/task_group/' + data.id;
      });
    }
  }, {});

})(window.can);
