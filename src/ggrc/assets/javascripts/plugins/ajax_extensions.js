/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/
(function($, can) {

  // Set up all PUT requests to the server to respect ETags, to ensure that
  // we are not overwriting more recent data than was viewed by the user.
  var etags = {};
  $.ajaxPrefilter(function(options, originalOptions, jqXHR) {
    var data = originalOptions.data;

    function attach_provisional_id(prop) {
      jqXHR.done(function(obj) {
        obj[prop].provisional_id = data[prop].provisional_id;
      });
    }

    if (/^\/api\//.test(options.url) && /PUT|POST|DELETE/.test(options.type.toUpperCase())) {
      options.dataType = "json";
      options.contentType = "application/json";
      jqXHR.setRequestHeader("If-Match", (etags[originalOptions.url] || [])[0]);
      jqXHR.setRequestHeader("If-Unmodified-Since", (etags[originalOptions.url] || [])[1]);
      options.data = options.type.toUpperCase() === "DELETE" ? "" : JSON.stringify(data);
      for (var i in data) {
        if (data.hasOwnProperty(i) && data[i] && data[i].provisional_id) {
          attach_provisional_id(i);
        }
      }
    }
    if (/^\/api\//.test(options.url) && (options.type.toUpperCase() === "GET")) {
      options.cache = false;
    }
    if (/^\/api\/\w+/.test(options.url)) {
      jqXHR.setRequestHeader("X-Requested-By", "gGRC");
      jqXHR.done(function(data, status, xhr) {
        if (!/^\/api\/\w+\/\d+/.test(options.url) && options.type.toUpperCase() === "GET")
          return;
        switch (options.type.toUpperCase()) {
          case "GET":
          case "PUT":
            etags[originalOptions.url] = [xhr.getResponseHeader("ETag"), xhr.getResponseHeader("Last-Modified")];
            break;
          case "POST":
            for (var d in data) {
              if (data.hasOwnProperty(d) && data[d].selfLink) {
                etags[data[d].selfLink] = [xhr.getResponseHeader("ETag"), xhr.getResponseHeader("Last-Modified")];
              }
            }
            break;
          case "DELETE":
            delete etags[originalOptions.url];
            break;
        }
      });
    }
  });

  //Set up default failure callbacks if nonesuch exist.
  var _old_ajax = $.ajax;

  var statusmsgs = {
    401: "The server says you are not authorized.  Are you logged in?",
    409: "There was a conflict in the object you were trying to update.  The version on the server is newer.",
    412: "One of the form fields isn't right.  Check the form for any highlighted fields."
  };


  // Here we break the deferred pattern a bit by piping back to original AJAX deferreds when we
  // set up a failure handler on a later transformation of that deferred.  Why?  The reason is that
  //  we have a default failure handler that should only be called if no other one is registered,
  //  unless it's also explicitly asked for.  If it's registered in a transformed one, though (after
  //  then() or pipe()), then the original one won't normally be notified of failure.
  can.ajax = $.ajax = function(options) {
    var _ajax = _old_ajax.apply($, arguments);

    function setup(_new_ajax, _old_ajax) {
      var _old_then = _new_ajax.then;
      var _old_fail = _new_ajax.fail;
      var _old_pipe = _new_ajax.pipe;
      _old_ajax && (_new_ajax.hasFailCallback = _old_ajax.hasFailCallback);
      _new_ajax.then = function() {
        var _new_ajax = _old_then.apply(this, arguments);
        if (arguments.length > 1) {
          this.hasFailCallback = true;
          if (_old_ajax)
            _old_ajax.fail(function() {});
        }
        setup(_new_ajax, this);
        return _new_ajax;
      };
      _new_ajax.fail = function() {
        this.hasFailCallback = true;
        if (_old_ajax)
          _old_ajax.fail(function() {});
        return _old_fail.apply(this, arguments);
      };
      _new_ajax.pipe = function() {
        var _new_ajax = _old_pipe.apply(this, arguments);
        setup(_new_ajax, this);
        return _new_ajax;
      };
    }

    setup(_ajax);
    return _ajax;
  };
})(jQuery, can);
