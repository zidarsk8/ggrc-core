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
          that = this,
          cycle;

      GGRC.Controllers.Modals.confirm({
        modal_title : "Confirm",
        modal_confirm : "Proceed",
        skip_refresh : true,
        button_view : GGRC.mustache_path + "/modals/confirm_buttons.mustache",
        content_view : GGRC.mustache_path + "/workflows/confirm_start.mustache",
        instance : GGRC.page_instance()
      }, function() {
        cycle = new CMS.Models.Cycle({
          context: page_instance.context.stub(),
          workflow: { id: page_instance.id, type: "Workflow" },
          autogenerate: true
        });

        cycle.save().then(function(cycle) {
          // Cycle created. Workflow started.
        });
      });
    },

    "[data-ggrc-action=end-cycle] click": function(el) {
      var $this = $(this)
        , options = $this.data('modal-selector-options');
      var workflow = $('button.end-cycle').closest('ul').control().options.parent_instance;
      var current_cycles = workflow.get_mapping('current_cycle');
      this.bindXHRToButton(function() {
        var dfds = [];
        if(current_cycles && current_cycles.length > 0) {
          for(var i = 0; i < current_cycles.length; i++) {
            dfds.push(current_cycles[i].instance.refresh().then(function(c) {
              return c.attr('is_current', false).save();
            }));
          }
        }
        return $.when.apply($, dfds).done(function() {
          return GGRC.page_instance().refresh();
        }).then(function(){
          // We need to update person's assigned_tasks mapping manually
          var person_id = GGRC.current_user.id,
              person = CMS.Models.Person.cache[person_id];
              binding = person.get_binding('assigned_tasks');

          // FIXME: Find a better way of removing stagnant items from the list.
          binding.list.splice(0, binding.list.length);
          return binding.loader.refresh_list(binding);
        });
      }(), el);
    },

    //  FIXME: This should trigger expansion of the TreeNode, without using
    //    global event listeners or routes or timeouts, but currently object
    //    creation and tree insertion is disconnected.
    "{CMS.Models.TaskGroup} created": function(model, ev, instance) {
      if (instance instanceof CMS.Models.TaskGroup) {
        setTimeout(function() {
          window.location.hash =
            'task_group_widget/task_group/' + instance.id;
        }, 250);
      }
    }
  });

})(this.CMS, this.GGRC, this.can, this.can.$);
