/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/


(function(can) {

  can.Model.Cacheable("CMS.Models.Workflow", {
    root_object: "workflow",
    root_collection: "workflows",
    category: "workflow",
    findAll: "GET /api/workflows",
    findOne: "GET /api/workflows/{id}",
    create: "POST /api/workflows",
    update: "PUT /api/workflows/{id}",
    destroy: "DELETE /api/workflows/{id}",
    attributes: {
      objects: "CMS.Models.get_stubs",
      workflow_objects: "CMS.Models.WorkflowObject.stubs",
      people: "CMS.Models.Person.stubs",
      workflow_people: "CMS.Models.WorkflowPerson.stubs",
      tasks: "CMS.Models.Task.stubs",
      workflow_tasks: "CMS.Models.WorkflowTask.stubs",
      task_groups: "CMS.Models.TaskGroup.stubs"
      //workflow_task_groups: "CMS.Models.WorkflowTaskGroup.stubs"
    },

    init: function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
    }
  }, {});

})(window.can);
