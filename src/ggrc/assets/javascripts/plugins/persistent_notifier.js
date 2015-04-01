/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/
(function(can) {
  can.Construct("PersistentNotifier", {
    defaults: {
      one_time_cbs: true,
      while_queue_has_elements: function() {},
      when_queue_empties: function() {}
    }
  }, {
    init: function(options) {
      var that = this;
      this.dfds = [];
      this.list_empty_cbs = [];
      can.each(this.constructor.defaults, function(val, key) {
        that[key] = val;
      });
      can.each(options, function(val, key) {
        that[key] = val;
      });
    },
    queue: function(dfd) {
      var idx,
        oldlen = this.list_empty_cbs.length,
        that = this;
      if (!dfd || !dfd.then) {
        throw "ERROR: attempted to queue something other than a Deferred or Promise";
      }
      idx = this.dfds.indexOf(dfd);

      if (!~idx) { //enforce uniqueness
        this.dfds.push(dfd);
        dfd.always(function() {
          var i = that.dfds.indexOf(dfd);
          ~i && that.dfds.splice(i, 1);
          if (that.dfds.length < 1) {
            can.each(that.list_empty_cbs, Function.prototype.call);
            if (that.one_time_cbs) {
              that.list_empty_cbs = [];
            }
            that.when_queue_empties();
          }
        });
      }
      if (oldlen < 1 && that.dfds.length > 0) {
        that.while_queue_has_elements();
      }
    },
    on_empty: function(fn) {
      if (!this.one_time_cbs || this.dfds.length < 1) {
        fn();
      }
      if ((this.dfds.length > 0 || !this.one_time_cbs) && !~this.list_empty_cbs.indexOf(fn)) {
        this.list_empty_cbs.push(fn);
      }
    },
    off_empty: function(fn) {
      var idx;
      if (~(idx = this.list_empty_cbs.indexOf(fn)))
        this.list_empty_cbs.splice(idx, 1);
    }
  });
})(can);
