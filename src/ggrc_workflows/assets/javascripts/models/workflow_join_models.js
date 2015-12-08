/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/


(function(can) {

  can.Model.Join("CMS.Models.TaskGroupObject", {
    root_object: "task_group_object",
    root_collection: "task_group_objects",
    join_keys: {
      "task_group": CMS.Models.TaskGroup,
      "object": can.Model.Cacheable,
    },
    attributes: {
      context: "CMS.Models.Context.stub",
      modified_by: "CMS.Models.Person.stub",
      task_group: "CMS.Models.TaskGroup.stub",
      object: "CMS.Models.get_stub",
    },
    findAll: "GET /api/task_group_objects",
    create: "POST /api/task_group_objects",
    update: "PUT /api/task_group_objects/{id}",
    destroy: "DELETE /api/task_group_objects/{id}"
  }, {
  });

  can.Model.Join("CMS.Models.WorkflowPerson", {
    root_object: "workflow_person",
    root_collection: "workflow_people",
    join_keys: {
      workflow: CMS.Models.Workflow,
      person: CMS.Models.Person,
    },
    attributes: {
      context: "CMS.Models.Context.stub",
      modified_by: "CMS.Models.Person.stub",
      workflow: "CMS.Models.Workflow.stub",
      person: "CMS.Models.Person.stub",
    },
    findAll: "GET /api/workflow_people",
    create: "POST /api/workflow_people",
    destroy: "DELETE /api/workflow_people/{id}",
  }, {
  });

})(window.can);
