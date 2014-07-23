/*
 */

(function(can) {

can.Model.Cacheable("CMS.Models.RiskAssessment", {
    root_object: "risk_assessment"
  , root_collection: "risk_assessments"
  , category: "risk_assessment"
  , findAll: "GET /api/risk_assessments"
  , findOne: "GET /api/risk_assessments/{id}"
  , create: "POST /api/risk_assessments"
  , update: "PUT /api/risk_assessments/{id}"
  , destroy: "DELETE /api/risk_assessments/{id}"
  , attributes: {
      ra_manager: "CMS.Models.Person.stub"
    , ra_counsel: "CMS.Models.Person.stub"
    , context: "CMS.Models.Context.stub"
    , program: "CMS.Models.Program.stub"
  }
  , init : function() {
      this._super && this._super.apply(this, arguments);
      this.validatePresenceOf("title");
      this.validatePresenceOf("start_date");
      this.validatePresenceOf("end_date");
    }
}, {});

})(window.can);
