/*
 */

(function(can) {

  _mustache_path = GGRC.mustache_path + "/risk_assessments";
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
      , documents : "CMS.Models.Document.stubs"
      , program: "CMS.Models.Program.stub"
      , modified_by: "CMS.Models.Person.stub"
      , object_documents: "CMS.Models.ObjectDocument.stubs"
    }
    , tree_view_options: {
      show_view: _mustache_path + "/tree.mustache",
      header_view: _mustache_path + "/tree_header.mustache",
      footer_view: _mustache_path + "/tree_footer.mustache",
      child_options: [{
        //0: Documents
        model: "Document",
        mapping: "documents",
        show_view: _mustache_path + "/documents.mustache",
        footer_view: _mustache_path + "/documents_footer.mustache"
      }],
    }
    , init : function() {
        this._super && this._super.apply(this, arguments);
        this.validateNonBlank("title");
        this.validateNonBlank("start_date");
        this.validateNonBlank("end_date");
      }
  }, {});

})(window.can);
