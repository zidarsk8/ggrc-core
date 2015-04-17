/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/

(function(can, $) {

  /*  GGRC.SaveQueue
   *
   *  SaveQueue is used by CMS.Models.Cacheable to prevent firing
   *  multiple requests to the server at once. It makes sure the requests
   *  are grouped together (inside _queue) and then resolved in batches.
   *
   *  enqueue(obj: CMS.Models.Cacheable, save_args) -> null
   */
  can.Construct("GGRC.SaveQueue", {

    DELAY: 100, // Number of ms to wait before the first batch is fired
    BATCH: 3,   // Maximum number of POST/PUT requests at any given time
    _queue: [],
    _timeout: null,

    enqueue: function (obj, args) {
     this._queue.push({o: obj, a: args});
     if (typeof this._timeout === "number") {
       clearTimeout(this._timeout);
     }
     this._timeout = setTimeout(function () {
       this._resolve();
     }.bind(this), this.DELAY);
    },
    _resolve: function() {
      if (!this._queue.length) {
        // Finished
        return;
      }
      var objs = this._queue.splice(0, this.BATCH), ret;
      $.when.apply($, objs.map(function (obj) {
        return obj.o._save.apply(obj.o, obj.a);
      })).always(function () {
        this._resolve(); // Move on to the next one
      }.bind(this));
    }
  }, {});

})(window.can, window.can.$);
