/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
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
          // If the TaskGroup was created as part of a Workflow, we don't want to
          //  do a redirect here
          if (instance._no_redirect) {
            return;
          }
          window.location.hash =
            'task_group_widget/task_group/' + instance.id;
        }, 250);
      }
    }
  });

  can.Model.Cacheable("CMS.ModelHelpers.CloneWorkflow", {
    defaults : {
      clone_people: true,
      clone_tasks: true,
      clone_objects: true
    }
  }, {
    refresh: function() {
      return $.when(this);
    },
    save: function() {
      var workflow = new CMS.Models.Workflow({
        clone: this.source_workflow.id,
        context: null,
        clone_people: this.clone_people,
        clone_tasks: this.clone_tasks,
        clone_objects: this.clone_objects
      });

      return workflow.save().then(function(workflow) {
        GGRC.navigate(workflow.viewLink);
        return this;
      });

    }
  });

  can.Model.Cacheable("CMS.ModelHelpers.CloneTaskGroup", {
    defaults : {
      clone_objects: true,
      clone_tasks: true,
      clone_people: true
    }
  }, {
    refresh: function() {
      return $.when(this);
    },
    save: function() {
      var task_group = new CMS.Models.TaskGroup({
        clone: this.source_task_group.id,
        context: null,
        clone_objects: this.clone_objects,
        clone_tasks: this.clone_tasks,
        clone_people: this.clone_people
      });

      return task_group.save();
    }
  });

})(this.CMS, this.GGRC, this.can, this.can.$);
