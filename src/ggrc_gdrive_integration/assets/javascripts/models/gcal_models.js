/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: brad@reciprocitylabs.com
 * Maintained By: brad@reciprocitylabs.com
 */

(function(can, $) {

  can.Model.Cacheable("CMS.Models.GCal", {

    findAll : function(params) {
      return GGRC.gapi_request_with_auth({
        path : "/calendar/v3/users/me/calendarList"
               + (params && params.id ? "/" + params.id : "")
               + "?"
               + $.param($.extend({ minAccessRole : "writer"}, params))
        , callback : function(dfd, result) {
          if(result.error) {
            dfd.reject(result.error);
          } else {
            var objs = result.items || [result];
            can.each(objs, function(obj) {
              obj.selfLink = obj.selfLink || "#";
            });
            dfd.resolve(objs);
          }
        }
      });
    }

    , getPrimary : function() {
      return GGRC.gapi_request_with_auth({
        path : "/calendar/v3/calendars/primary",
        callback : function(dfd, d) { dfd.resolve(d); }
      });
    }

  }, {

    eventsModel : function() {
      var that = this;
      return CMS.Models.GCalEvent.extend({
        getPath : function() {
          return "/calendar/v3/calendars/" + that.id + "/events";
        }
      }, {});
    }

  });



  can.Model.Cacheable("CMS.Models.GCalEvent", {

    getPath : function(params) {
      return "/calendar/v3/calendars/" + (params && params.calendar ? params.calendar.id : GGRC.config.DEFAULT_CALENDAR.id) + "/events";
    }

    , findAll : function(params) {
      var q = "";
      if(params && params.response) {
        q = "PBC Response #" + params.response.id;
      }
      return GGRC.gapi_request_with_auth({
        path : this.getPath(params) + "?q=" + encodeURIComponent(q)
        , method : "get"
        , callback : function(dfd, result) {
          if(result.error) {
            dfd.reject(result.error);
          } else {
            var objs = result.items;
            can.each(objs, function(obj) {
              obj.selfLink = obj.selfLink || "#";
            });
            dfd.resolve(objs);
          }
        }
      });
    }
    , create : function(params) {
      return GGRC.gapi_request_with_auth({
        path : this.getPath(params)
        , body : params
        , method : "post"
        , callback : function(dfd, d) {
          dfd.resolve(d);
        }
      });
    }
    , destroy : function(id) {
      return GGRC.gapi_request_with_auth({
        path : this.getPath() + "/" + id
        , method : "delete"
        , callback : function(dfd, d) {
          dfd.resolve(d);
        }
      });
    }
    , attributes : {
      start : "packaged_datetime"
      , end : "packaged_datetime"
      , attendees: "email_only"
    }
    , serialize : {
      email_only : function(val) {
        if(val.reify) {
          return can.map(val.reify(), function(p) { return {email : p.email}; });
        }
      }
    }
    , convert : {
      email_only : function(val) {
        var cache = {}
        , finds = []
        , result = new CMS.Models.Person.List();
        can.each(Object.keys(CMS.Models.Person.cache), function(id) {
          var person = CMS.Models.Person.cache[id];
          if(person.email) {
            cache[person.email] = person;
          }
        });
        can.each(val, function(g_person) {
          if(cache[g_person.email]) {
            result.push(cache[g_person.email]);
          } else {
            finds.push(g_person.email);
          }
        });
        if(finds.length > 0) {
          CMS.Models.Person.findAll({"email__in" : finds.join(",") }).done(function(np) {
            result.push.apply(result, np);
          });
        }
        return result;
      }
    }
  }, {
    serialize : function(attr) {
          var serial;
    if(!attr) {
      serial = this._super.apply(this, arguments);
      serial.event_id = serial.event ? serial.event.id : serial.event_id;
      delete serial.event;
      serial.calendar_id = serial.calendar ? serial.calendar.id : serial.calendar_id;
      delete serial.calendar;
      return serial;
    }
      if(attr === "attendees") {
        return can.map((this.attendees || new can.Model.List()).reify(), function(p) { return {email : p.email}; });
      }
      return 
    }
  });

can.Model.Join("CMS.Models.ObjectEvent", {
  root_object : "object_event"
  , root_collection : "object_events"
  , findAll: "GET /api/object_events?__include=event"
  , create : "POST /api/object_events"
  , update : "PUT /api/object_events/{id}"
  , destroy : "DELETE /api/object_events/{id}"
  , join_keys : {
    eventable : can.Model.Cacheable
    , event : CMS.Models.GCalEvent
  }
  , attributes : {
      modified_by : "CMS.Models.Person.stub"
    , event : "CMS.Models.GCalEvent.stub"
    , eventable : "CMS.Models.get_stub"
    , calendar : "CMS.Models.GCal.stub"
  }

  , model : function(params) {
    if(typeof params === "object") {
      params.event = {
        id : params.event_id
        , type : "GCalEvent"
        , calendar_id : params.calendar_id
        , href : "/calendar/v3/calendars/" + params.calendar_id + "/events/" + params.event_id
      };
    }
    return this._super(params);
  }
}, {

  serialize : function(attr) {
    var serial;
    if(!attr) {
      serial = this._super.apply(this, arguments);
      serial.event_id = serial.event ? serial.event.id : serial.event_id;
      delete serial.event;
      serial.calendar_id = serial.calendar ? serial.calendar.id : serial.calendar_id;
      delete serial.calendar;
      return serial;
    }
    switch(attr) {
      case "event":
        return this.event_id || this.event.id;
      case "calendar":
        return this.calendar_id || this.calendar.id;
      default:
        return this._super.apply(this, arguments);
    }
  }
});
})(this.can, this.can.$);
