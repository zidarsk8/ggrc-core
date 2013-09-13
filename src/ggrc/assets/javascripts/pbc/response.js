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
  }
  , create : "POST /api/responses"
  , update : "PUT /api/responses/{id}"

  , findAll : "GET /api/responses"
  , destroy : "DELETE /responses/{id}"
  , attributes : {
    owner : "CMS.Models.Person.model"
    , object_people : "CMS.Models.ObjectPerson.models"
    , people : "CMS.Models.Person.models"
    , object_documents : "CMS.Models.ObjectDocument.models"
    , documents : "CMS.Models.Document.models"
    , population_sample : "CMS.Models.PopulationSample.model"
    , meetings : "CMS.Models.Meeting.models"
  }
}, {
});