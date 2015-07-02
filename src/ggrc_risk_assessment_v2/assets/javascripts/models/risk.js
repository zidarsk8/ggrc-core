/*
 * Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
 * Unauthorized use, copying, distribution, displaying, or public performance
 * of this file, via any medium, is strictly prohibited. All information
 * contained herein is proprietary and confidential and may not be shared
 * with any third party without the express written consent of Reciprocity, Inc.
 * Created By: silas@reciprocitylabs.com
 * Maintained By: silas@reciprocitylabs.com
 */


(function(can) {

  can.Model.Cacheable("CMS.Models.Risk", {
    root_object: "risk",
    root_collection: "risks",
    category: "risk",
    findAll: "GET /api/risks",
    findOne: "GET /api/risks/{id}",
    create: "POST /api/risks",
    update: "PUT /api/risks/{id}",
    destroy: "DELETE /api/risks/{id}",
    mixins: ["ownable", "contactable", "unique_title"],
    is_custom_attributable: true,
    attributes : {
      context : "CMS.Models.Context.stub",
      contact : "CMS.Models.Person.stub",
      owners : "CMS.Models.Person.stubs",
      modified_by : "CMS.Models.Person.stub",
      objects : "CMS.Models.get_stubs",
      risk_objects: "CMS.Models.RiskObject.stubs"
    },
    tree_view_options: {},

    init: function() {
      this._super && this._super.apply(this, arguments);
      var req_fields = ["title", "description", "contact", "owners"];
      for (var i = 0; i < req_fields.length; i++) {
        this.validatePresenceOf(req_fields[i]);
      }
    }
  }, {});

})(window.can);
