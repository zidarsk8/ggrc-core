/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: andraz@reciprocitylabs.com
    Maintained By: andraz@reciprocitylabs.com
*/

;(function(CMS, GGRC, can, $) {
  var MIN_WAIT = 2000,
      MAX_WAIT = 5000;

  var refresher = {
    instanceQueue: [],
    lastRefresh: Date.now(),
    refreshInstance: function(instance) {
      this.instanceQueue.push(instance);
      setTimeout(this.tick(instance), MIN_WAIT);
    },
    tick: function(instance) {
      return (function(){
        var isCurrent = this.instanceQueue[this.instanceQueue.length - 1] === instance;
        var isOverdue = (this.lastRefresh + MAX_WAIT) < Date.now();
        if (isCurrent || isOverdue) {
          this.go();
        }
      }).bind(this);
    },
    go: function() {
      this.lastRefresh = Date.now();
      var instances = this.instanceQueue;
      this.instanceQueue = [];

      var ids = $.map(instances, function(instance) {
        return instance.id;
      });
      var filter = {automapping_id__in: ids.join()};
      CMS.Models.Relationship.findAll(filter).then(function(relationships) {
        var rq = new RefreshQueue();
        can.each(relationships.concat(instances), function(relationship) {
          rq.enqueue(relationship.source);
          rq.enqueue(relationship.destination);
        });
        rq.trigger();
      });
    }
  };

  var flashWarning = function() {
    // timeout is required because a "mapping created" success flash will show up
    // and we do not currently support multiple simultaneous flashes
    setTimeout(function() {
      $(document.body).trigger("ajax:flash", {
        "warning": "Automatic mappings were not created because that would result in too many new mappings"
      });
    }, 2000); // 2000 is a magic number that feels nice in the UI
  };

  var Controller = can.Control({
    "{CMS.Models.Relationship} created": function(model, ev, instance) {
      if (instance instanceof CMS.Models.Relationship) {
        var limit_exceeded = instance.extras && instance.extras.automapping_limit_exceeded;
        if (limit_exceeded) {
          flashWarning();
        } else {
          refresher.refreshInstance(instance);
        }
      }
    }
  });

  $(function() {
    new Controller();
  });
})(this.CMS, this.GGRC, this.can, this.can.$);

