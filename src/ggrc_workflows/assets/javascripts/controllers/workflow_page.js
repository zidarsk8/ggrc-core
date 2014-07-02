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
      var page_instance = GGRC.page_instance()
        , that = this
        , cycle;

      GGRC.Controllers.Modals.confirm({
        modal_title : "Confirm"
        , modal_confirm : "Proceed"
        , skip_refresh : true
        , button_view : GGRC.mustache_path + "/modals/confirm_buttons.mustache"
        , content_view : GGRC.mustache_path + "/workflows/confirm_start.mustache"
        , instance : GGRC.page_instance()
      }, function() {
        cycle = new CMS.Models.Cycle({
          context: { id: null, type: "Context" },
          workflow: { id: page_instance.id, type: "Workflow" },
          autogenerate: true
        });

        cycle.save().then(function(cycle) {
          // Cycle created. Workflow started.
        });
      });
    },

    "[data-ggrc-action=end-cycle] click": function() {

    },
  });

})(this.CMS, this.GGRC, this.can, this.can.$);
