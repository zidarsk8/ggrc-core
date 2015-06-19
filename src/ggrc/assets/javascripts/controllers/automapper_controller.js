/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: andraz@reciprocitylabs.com
    Maintained By: andraz@reciprocitylabs.com
*/

;(function(CMS, GGRC, can, $) {
  var Controller = can.Control({
    "{CMS.Models.Relationship} created": function(model, ev, instance) {
      if (instance instanceof CMS.Models.Relationship) {
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
    }
  });
  $(function(){
    new Controller();
  });
})(this.CMS, this.GGRC, this.can, this.can.$);

