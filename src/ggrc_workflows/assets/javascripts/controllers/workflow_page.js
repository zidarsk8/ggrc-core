/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/

;(function(CMS, GGRC, can, $) {

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
      click: function() {
        var page_instance = GGRC.page_instance(),
            that = this,
            cycle;

        GGRC.Controllers.Modals.confirm({
          modal_title : "Confirm",
          modal_confirm : "Proceed",
          skip_refresh : true,
          button_view : GGRC.mustache_path + "/workflows/confirm_start_buttons.mustache",
          content_view : GGRC.mustache_path + "/workflows/confirm_start.mustache",
          instance : GGRC.page_instance()
        }, function(params, option) {
          var data = {},
              d = new Date(),
              base_date,
              workflow = page_instance;

          can.each(params, function(item) {
            data[item.name] = item.value;
          });

          if (option === 'this') {
            base_date = moment().format('MM/DD/YYYY');
          }
          else if (option === 'next') {
            base_date = moment().add(1,
              workflow.frequency_duration()).format('MM/DD/YYYY');
          }

          cycle = new CMS.Models.Cycle({
            context: page_instance.context.stub(),
            workflow: { id: page_instance.id, type: "Workflow" },
            start_date: base_date || null,
            autogenerate: true
          });

          cycle.save().then(function(cycle) {
            // Cycle created. Workflow started.
            setTimeout(function() {
              window.location.hash = 'current_widget/cycle/' + cycle.id;
            }, 250);
          });
        });
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
