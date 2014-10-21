/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: laran@reciprocitylabs.com
    Maintained By: laran@reciprocitylabs.com
*/

//= require can.jquery-all
//= require models/cacheable
(function(namespace, $){
can.Model.Cacheable("CMS.Models.CustomAttributeDefinition", {
  // static properties
    root_object : "custom_attribute_definition"
  , root_collection : "custom_attribute_definitions"
  , category : "custom_attribute_definitions"
  , findOne : "GET /api/custom_attribute_definitions/{id}"
  , create : "POST /api/custom_attribute_definitions"
  , update : "PUT /api/custom_attribute_definitions/{id}"
  , destroy : "DELETE /api/custom_attribute_definitions/{id}"
  , mixins : []
  , attributes : {
    values : "CMS.Models.CustomAttributeValue.stubs"
    , modified_by : "CMS.Models.Person.stub"
  }
  , links_to : {
  }

  , defaults : {
    "title" : ""
  }

  , tree_view_options : {
      show_view : GGRC.mustache_path + "/custom_attributes/tree.mustache"
    , footer_view : GGRC.mustache_path + "/custom_attributes/tree_footer.mustache"
    , draw_children : true
  }

  , init : function() {
    //this.validateNonBlank("title");
    this._super.apply(this, arguments);
  }
}
, {
  init : function() {
    var that = this;
    this._super.apply(this, arguments);
  }
});

})(this, can.$);

(function(namespace, $){
can.Model.Cacheable("CMS.Models.CustomAttributeValue", {
  // static properties
    root_object : "custom_attribute_value"
  , root_collection : "custom_attribute_values"
  , category : "custom_attribute_values"
  , findOne : "GET /api/custom_attribute_values/{id}"
  , create : "POST /api/custom_attribute_values"
  , update : "PUT /api/custom_attribute_values/{id}"
  , destroy : "DELETE /api/custom_attribute_values/{id}"
  , mixins : []
  , attributes : {
    definition : "CMS.Models.CustomAttributeDefinition.stub"
    , modified_by : "CMS.Models.Person.stub"
  }
  , links_to : {
  }
  , defaults : {
    "title" : ""
  }
  , init : function() {
    //this.validateNonBlank("title");
    this._super.apply(this, arguments);
  }
}
, {
  init : function() {
    var that = this;
    this._super.apply(this, arguments);
  }
});

})(this, can.$);
