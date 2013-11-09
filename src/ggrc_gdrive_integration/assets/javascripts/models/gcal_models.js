
(function(can, $) {

  can.Model.Cacheable("CMS.Models.GCal", {

    findAll : function(params) {
      return window.oauth_dfd.then(function() {
        var dfd = new $.Deferred();
        gapi.client.request({
          path : "/calendar/v3/users/me/calendarList"
                 + (params && params.id ? "/" + params.id : "")
                 + "?"
                 + $.param($.extend({ minAccessRole : "writer"}, params))
          , callback : function(result) {
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
        return dfd;
      });
    }

    , getPrimary : function() {
      return window.oauth_dfd.then(function() {
        var dfd = new $.Deferred();
        gapi.client.request({
          path : "/calendar/v3/calendars/primary",
          callback : function(d) { dfd.resolve(d); }
        });
        return dfd.promise();
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
      var that = this;
      return window.oauth_dfd.then(function() {
        var q = "", dfd = new $.Deferred();
        if(params && params.response) {
          q = "PBC Response #" + params.response.id;
        }
        gapi.client.request({
          path : that.getPath(params) + "?q=" + encodeURIComponent(q)
          , method : "get"
          , callback : function(result) {
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
        return dfd;
      });
    }
    , create : function(params) {
      var that = this;
      return window.oauth_dfd.then(function() {
        var dfd = new $.Deferred();
        gapi.client.request({
          path : that.getPath(params)
          , body : params
          , method : "post"
          , callback : function(d) {
            dfd.resolve(d);
          }
        });
        return dfd.promise();
      });
    }
    , destroy : function(id) {
      var that = this;
      return window.oauth_dfd.then(function() {
        var dfd = new $.Deferred();
        gapi.client.request({
          path : that.getPath() + "/" + id
          , method : "delete"
          , callback : function(d) {
            dfd.resolve(d);
          }
        });
        return dfd.promise();
      });
    }
    , attributes : {
      start : "packaged_datetime"
      , end : "packaged_datetime"
    }
  }, {

  });

})(this.can, this.can.$);