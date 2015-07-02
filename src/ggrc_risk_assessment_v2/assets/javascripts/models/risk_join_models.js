/*
 * Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
 * Unauthorized use, copying, distribution, displaying, or public performance
 * of this file, via any medium, is strictly prohibited. All information
 * contained herein is proprietary and confidential and may not be shared
 * with any third party without the express written consent of Reciprocity, Inc.
 * Created By: anze@reciprocitylabs.com
 * Maintained By: anze@reciprocitylabs.com
 */


(function(can) {

  can.Model.Join("CMS.Models.RiskObject", {
    root_object: "risk_object",
    root_collection: "risk_objects",
    join_keys: {
      "risk": CMS.Models.Risk,
      "object": can.Model.Cacheable,
    },
    attributes: {
      context: "CMS.Models.Context.stub",
      modified_by: "CMS.Models.Person.stub",
      risk: "CMS.Models.Risk.stub",
      object: "CMS.Models.get_stub",
    },
    findAll: "GET /api/risk_objects",
    create: "POST /api/risk_objects",
    destroy: "DELETE /api/risk_objects/{id}"
  }, {
  });

})(window.can);
