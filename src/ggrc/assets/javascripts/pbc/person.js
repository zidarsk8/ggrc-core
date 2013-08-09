/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require models/cacheable

(function(ns, can) {

can.Model.Cacheable("CMS.Models.Person", {
   root_object : "person"
   , root_collection : "people"
   , findAll : "GET /api/people"
   , findOne : "GET /api/people/{id}"
   , create : "POST /api/people"
   , update : "PUT /api/people/{id}"
   , destroy : "DELETE /api/people/{id}"
    , search : function(request, response) {
        return $.ajax({
            type : "get"
            , url : "/api/people"
            , dataType : "json"
            , data : {s : request.term}
            , success : function(data) {
                response($.map( data, function( item ) {
                  return can.extend({}, item.person, {
                    label: item.person.email
                    , value: item.person.id
                  });
                }));
            }
        });
    }
}, {
    init : function () {
        this._super && this._super();
        // this.bind("change", function(ev, attr, how, newVal, oldVal) {
        //     var obj;
        //     if(obj = CMS.Models.ObjectPerson.findInCacheById(this.id) && attr !== "id") {
        //         obj.attr(attr, newVal);
        //     }
        // });

        var that = this;

        this.each(function(value, name) {
          if (value === null)
            that.removeAttr(name);
        });
    }
  , display_name : function() {
    return this.email;
  }
});


can.Model.Cacheable("CMS.Models.ObjectPerson", {
    root_object : "object_person"
    , root_collection : "object_people"
    , findAll: "GET /api/object_people"
    , create : "POST /api/object_people"
    , update : "PUT /api/object_people/{id}"
    , destroy : "DELETE /api/object_people/{id}"
}, {
    init : function() {
        var _super = this._super;
        function reinit() {
            var that = this;

            typeof _super === "function" && _super.call(this);
            this.attr("person", CMS.Models.get_instance(
                  "Person", this.person_id || (this.person && this.person.id)));
            this.attr("personable", CMS.Models.get_instance(
                  this.personable_type || (this.personable && this.personable.type),
                  this.personable_id || (this.personable && this.personable.id)));

            this.each(function(value, name) {
              if (value === null)
              that.removeAttr(name);
            });
        }

        this.bind("created", can.proxy(reinit, this));

        reinit.call(this);
    }
});

})(this, can);
