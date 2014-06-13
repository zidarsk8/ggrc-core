/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/

;(function(CMS, GGRC, can, $) {

  can.Control("GGRC.Controllers.WorkflowPage", {
    defaults: {
    },

    init: function() {
      if (this._super) {
        this._super.apply(this, arguments);
      }
    }
  }, {
    init: function() {
      this._super.apply(this, arguments);
    },

    "[data-ggrc-action=start-cycle] click": function() {
      var page_instance = GGRC.page_instance(),
          cycle;

      cycle = new CMS.Models.Cycle({
        context: { id: null, type: "Context" },
        workflow: { id: page_instance.id, type: "Workflow" },
        autogenerate: true
      });

      cycle.save().then(function(cycle) {
        //console.debug("done", arguments);
      });
      //console.debug("creating", arguments);
    },

    "[data-ggrc-action=end-cycle] click": function() {
      //console.debug(arguments);
    }
  });

})(this.CMS, this.GGRC, this.can, this.can.$);
