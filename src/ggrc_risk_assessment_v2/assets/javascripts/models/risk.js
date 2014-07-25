/*!
 Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: silas@reciprocitylabs.com
 Maintained By: silas@reciprocitylabs.com
*/


(function(can) {

  can.Model.Cacheable("CMS.Models.Risk", {
    root_object: "risk",
    root_collection: "risks",
    category: "risk_assessment_v2",
    findAll: "GET /api/risks",
    findOne: "GET /api/risks/{id}",
    create: "POST /api/risks",
    update: "PUT /api/risks/{id}",
    destroy: "DELETE /api/risks/{id}",
    mixins: ["ownable", "contactable"],
    attributes : {
      context : "CMS.Models.Context.stub",
      contact : "CMS.Models.Person.stub",
      owners : "CMS.Models.Person.stubs",
      modified_by : "CMS.Models.Person.stub"
    },
    tree_view_options: {},

    init: function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
    }
  }, {});

})(window.can);
