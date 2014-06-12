/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/


(function(can) {

  can.Model.Cacheable("CMS.Models.Task", {
    root_object: "task",
    root_collection: "tasks",
    category: "workflow",
    findAll: "GET /api/tasks",
    findOne: "GET /api/tasks/{id}",
    create: "POST /api/tasks",
    update: "PUT /api/tasks/{id}",
    destroy: "DELETE /api/tasks/{id}",

    attributes: {
      modified_by: "CMS.Models.Person.stub"
    },
    tree_view_options: {
      //show_view: GGRC.mustache_path + "/tasks/tree.mustache",
      footer_view: GGRC.mustache_path + "/tasks/tree_footer.mustache"
    },

    init: function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
    }
  }, {});

})(window.can);
