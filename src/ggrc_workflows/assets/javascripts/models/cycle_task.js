/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/


(function(can) {

  can.Model.Cacheable("CMS.Models.CycleTask", {
    root_object: "cycle_task",
    root_collection: "cycle_tasks",
    category: "workflow",
    findAll: "GET /api/cycle_tasks",
    findOne: "GET /api/cycle_tasks/{id}",
    create: "POST /api/cycle_tasks",
    update: "PUT /api/cycle_tasks/{id}",
    destroy: "DELETE /api/cycle_tasks/{id}",

    attributes: {
      modified_by : "CMS.Models.Person.stub"
    },
    tree_view_options: {
      //show_view: GGRC.mustache_path + "/cycle_tasks/tree.mustache",
      footer_view: GGRC.mustache_path + "/cycle_tasks/tree_footer.mustache"
    },

    init: function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
    }
  }, {});

})(window.can);
