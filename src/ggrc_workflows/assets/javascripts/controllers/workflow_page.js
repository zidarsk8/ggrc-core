/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/

;(function(CMS, GGRC, can, $) {

  function _generate_cycle() {
    var workflow = GGRC.page_instance(),
        dfd = new $.Deferred(),
        cycle;

    GGRC.Controllers.Modals.confirm({
      modal_title : "Confirm",
      modal_confirm : "Proceed",
      skip_refresh : true,
      button_view : GGRC.mustache_path + "/modals/confirm_buttons.mustache",
      content_view : GGRC.mustache_path + "/workflows/confirm_start.mustache",
      instance : workflow
    }, function(params) {
      var data = {};

      can.each(params, function(item) {
        data[item.name] = item.value;
      });

      cycle = new CMS.Models.Cycle({
        context: workflow.context.stub(),
        workflow: { id: workflow.id, type: "Workflow" },
        start_date: data.base_date || null,
        autogenerate: true
      });

      cycle.save().then(function(cycle) {
        // Cycle created. Workflow started.
        setTimeout(function() {
          dfd.resolve();
          window.location.hash = 'current_widget/cycle/' + cycle.id;
        }, 250);
      });
    }, function() {
      dfd.reject();
    });
    return dfd;
  }

  can.Control("GGRC.Controllers.WorkflowPage", {
    defaults: {
    }
  }, {
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

  can.Component.extend({
    tag: "workflow-start-cycle",
    content: "<content/>",
    events: {
      click: _generate_cycle
    }
  });

  can.Component.extend({
    tag: "workflow-activate",
    template: "<content/>",
    events: {
      click: function() {
        var workflow = GGRC.page_instance();
        if (workflow.frequency !== 'one_time') {
          workflow.refresh().then(function() {
            workflow.attr('status', "Active").save();
          });
        } else {
          _generate_cycle().then(function() {
            workflow.refresh().then(function() {
              workflow.attr('status', "NoRecurrences").save();
            });
          });
        }
      }
    }
  });

  can.Component.extend({
    tag: "workflow-deactivate",
    template: "<content/>",
    events: {
      click: function() {
        var workflow = GGRC.page_instance();
        workflow.attr('status', "NoRecurrences").save();
      }
    }
  });

  can.Component.extend({
    tag: "workflow-clone",
    template: "<content/>",
    events: {
      click: function() {
        var workflow;

        workflow = new CMS.Models.Workflow({
          clone: this.scope.workflow.id,
          context: null
        });

        workflow.save().then(function(workflow) {
          window.location.href = workflow.viewLink;
        });
      }
    }
  });

  can.Component.extend({
    tag: "cycle-end-cycle",
    template: "<content/>",
    events: {
      click: function() {
        this.scope.cycle.refresh().then(function(cycle) {
          cycle.attr('is_current', false).save().then(function() {
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
        });
      }
    }
  });

})(this.CMS, this.GGRC, this.can, this.can.$);
