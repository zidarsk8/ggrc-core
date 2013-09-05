/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable

(function(ns, can) {

can.Model.Cacheable("CMS.Models.Document", {
    root_object : "document"
    , root_collection : "documents"
    , title_singular : "Reference"
    , title_plural : "References"
    , findAll : "GET /api/documents"
    , create : "POST /api/documents"
    , update : "PUT /api/documents/{id}"
    , destroy : "DELETE /api/documents/{id}"
    , search : function(request, response) {
        return $.ajax({
            type : "get"
            , url : "/api/documents"
            , dataType : "json"
            , data : {s : request.term}
            , success : function(data) {
                response($.map( data, function( item ) {
                  return can.extend({}, item.document, {
                    label: item.document.title 
                          ? item.document.title 
                          + (item.document.link_url 
                            ? " (" + item.document.link_url + ")" 
                            : "")
                          : item.document.link_url
                    , value: item.document.id
                  });
                }));
            }
        });
    }
    , attributes : {
        object_documents : "CMS.Models.ObjectDocument.models"
      , type : "CMS.Models.Option.model"
      , kind : "CMS.Models.Option.model"
      , year : "CMS.Models.Option.model"
    }
  , tree_view_options: {
        list_view: GGRC.mustache_path + "/documents/tree.mustache"
    }
  , init : function() {
    this.validatePresenceOf("link");
    this._super.apply(this, arguments);
  }

}, {
});

})(this, can);
