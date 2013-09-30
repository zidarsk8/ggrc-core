/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require pbc/system
//= require pbc/population_sample
//= require pbc/meeting

can.Model.Cacheable("CMS.Models.Response", {

  root_object : "response"
  , root_collection : "responses"
  , init : function() {
    this._super && this._super.apply(this, arguments);

    CMS.Models.Meeting.bind("destroyed", function(ev, mtg){
      can.each(CMS.Models.Response.cache, function(response) {
        response.removeElementFromChildList("meetings", mtg);
      });
    });
    this.cache = {};
  }
  , create : "POST /api/responses"
  , update : "PUT /api/responses/{id}"

  , findAll : "GET /api/responses"
  , destroy : "DELETE /responses/{id}"
  , model : function(params) {
    if (this.shortName !== 'Response')
      return this._super(params);
    if (!params)
      return params;
    params = this.object_from_resource(params);
    if (!params.selfLink) {
      if (params.type !== 'Response')
        return CMS.Models[params.type].model(params);
    } else {
      if (CMS.Models.DocumentationResponse.root_object === params.response_type + "_response")
        return CMS.Models.DocumentationResponse.model(params);
      else if (CMS.Models.InterviewResponse.root_object === params.response_type + "_response")
        return CMS.Models.InterviewResponse.model(params);
      else if (CMS.Models.PopulationSampleResponse.root_object === params.response_type + "_response")
        return CMS.Models.PopulationSampleResponse.model(params);
    }
    console.debug("Invalid Response:", params);
  }
  , attributes : {
    owner : "CMS.Models.Person.model"
    , object_people : "CMS.Models.ObjectPerson.stubs"
    , people : "CMS.Models.Person.stubs"
    , object_documents : "CMS.Models.ObjectDocument.stubs"
    , documents : "CMS.Models.Document.stubs"
    , population_sample : "CMS.Models.PopulationSample.stub"
    , meetings : "CMS.Models.Meeting.stubs"
    , participants : "CMS.Models.Person.stubs"
    , request : "CMS.Models.Request.stub"
    , assignee : "CMS.Models.Person.stub"
  }
  , tree_view_options : {
    show_view : GGRC.mustache_path + "/responses/tree.mustache"
    , footer_view : GGRC.mustache_path + "/responses/tree_footer.mustache"
    , draw_children : true
    , child_options : [{
      //0: mapped objects
      mapper : "Relationships"
      , model : can.Model.Cacheable
    }, {
      //1: Document Evidence
      model : "Document"
    }, {
      //2: Meetings
      model : "Meeting"
      , show_view : GGRC.mustache_path + "/meetings/tree.mustache"
      , footer_view : GGRC.mustache_path + "/meetings/tree_footer.mustache"
    }, {
      //3: Meeting participants
      model : "Person"
    }]
  }
}, {
});

CMS.Models.Response("CMS.Models.DocumentationResponse", {
  root_object : "documentation_response"
  , root_collection : "documentation_responses"
  , create : "POST /api/documentation_responses"
  , update : "PUT /api/documentation_responses/{id}"
  , findAll : "GET /api/documentation_responses"
  , attributes : {}
  , init : function() {
    this._super && this._super.apply(this, arguments);
    can.extend(this.attributes, CMS.Models.Response.attributes);
    this.cache = CMS.Models.Response.cache;
  }
}, {});

CMS.Models.Response("CMS.Models.InterviewResponse", {
  root_object : "interview_response"
  , root_collection : "interview_responses"
  , create : "POST /api/interview_responses"
  , update : "PUT /api/interview_responses/{id}"
  , findAll : "GET /api/interview_responses"
  , attributes : {}
  , init : function() {
    this._super && this._super.apply(this, arguments);
    can.extend(this.attributes, CMS.Models.Response.attributes);
    this.cache = CMS.Models.Response.cache;
  }
}, {});

CMS.Models.Response("CMS.Models.PopulationSampleResponse", {
  root_object : "population_sample_response"
  , root_collection : "population_sample_responses"
  , create : "POST /api/population_sample_responses"
  , update : "PUT /api/population_sample_responses/{id}"
  , findAll : "GET /api/population_sample_responses"
  , attributes : {}
  , init : function() {
    this._super && this._super.apply(this, arguments);
    can.extend(this.attributes, CMS.Models.Response.attributes);
    this.cache = CMS.Models.Response.cache;
  }
}, {});