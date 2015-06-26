/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: andraz@reciprocitylabs.com
    Maintained By: andraz@reciprocitylabs.com
*/

;(function(CMS, GGRC, can, $) {
  function flashWarning() {
    // timeout is required because a "mapping created" success flash will show up
    // and we do not currently support multiple simultaneous flashes
    setTimeout(function() {
      $(document.body).trigger("ajax:flash", {
        "warning": "Automatic mappings were not created because that would result in too many new mappings"
      });
    }, 2000); // 2000 is a magic number that feels nice in the UI
  }
  
  function refreshAutomappings(instance) {
    CMS.Models.Relationship.findAll({automapping_id: instance.id}).then(function(relationships) {
      var rq = new RefreshQueue();
      rq.enqueue(instance.source);
      rq.enqueue(instance.destination);
      can.each(relationships, function(relationship) {
        rq.enqueue(relationship.source);
        rq.enqueue(relationship.destination);
      });
      rq.trigger();
    });
  }
  
  var Controller = can.Control({
    "{CMS.Models.Relationship} created": function(model, ev, instance) {
      if (instance instanceof CMS.Models.Relationship) {
        var limit_exceeded = instance.extras && instance.extras.automapping_limit_exceeded;
        if (limit_exceeded) {
          flashWarning()
        } else {
          refreshAutomappings(instance);
        }
      }
    }
  });
  
  $(function() {
    new Controller();
  });
})(this.CMS, this.GGRC, this.can, this.can.$);

