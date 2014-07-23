/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

;(function(can, $, GGRC, CMS) {
  
can.Observe("CMS.ModelHelpers.ApprovalWorkflow", {
  defaults : {
    original_object: null,
  }
}, {
  save : function() {
    var that = this;
    return $.when(
      new CMS.Models.Workflow({
        frequency: "one_time",
        title: "Object review for "
                + this.original_object.constructor.title_singular
                + ' "' + this.original_object.title + '"',
        start_date: new Date(),
        end_date: this.end_date,
        object_approval: true,
        notify_on_change: true,
        notify_custom_message: "Hello " + this.contact.reify().name + ",\n\n"
          + GGRC.current_user.name + " (" + GGRC.current_user.email 
          + ") asked you to review newly created "
          + this.original_object.constructor.model_singular + ' "' + this.original_object.title
          + '" before ' + moment(this.end_date).format("MM/DD/YYYY") + ". "
          + "Click <a href='" + window.location.href.replace("#.*$", "#") 
          + "workflows_widget'>here</a> to perform a review.\n\nThanks,\ngGRC Team",
        context: that.original_object.context
      }).save(),
      CMS.Models.Task.findAll({title : "Object review"})
    ).then(function(wf, tasks) {
      if (tasks.length < 1) {
        return $.when(
          wf,
          new CMS.Models.Task({
            title: "Object review for "
                    + that.original_object.constructor.title_singular
                    + ' "' + that.original_object.title + '"',
            context: {id : null}
          }).save()
        );
      } else {
        return $.when(wf, tasks[0]);
      }
    }).then(function(wf, task) {
      return $.when(
        wf,
        task,
        new CMS.Models.TaskGroup({
          workflow : wf,
          title: "Object review for "
                  + that.original_object.constructor.title_singular
                  + ' "' + that.original_object.title + '"',
          contact: that.contact,
          context: wf.context
        }).save(),
        new CMS.Models.WorkflowObject({
          workflow: wf,
          object: that.original_object,
          context: wf.context
        }).save(),
        new CMS.Models.WorkflowTask({
          workflow: wf,
          task: task,
          context: wf.context
        }).save(),
        new CMS.Models.WorkflowPerson({
          workflow: wf,
          person: that.contact,
          context: wf.context
        }).save()
      );
    }).then(function(wf, task, tg) {
      return $.when(
        wf,
        new CMS.Models.TaskGroupTask({
          task_group: tg,
          task: task,
          sort_index: Number.MAX_SAFE_INTEGER / 2,
          contact: that.contact,
          context: wf.context
        }).save(),
        new CMS.Models.TaskGroupObject({
          task_group: tg,
          object: that.original_object,
          context: wf.context
        }).save()
      );
    }).then(function(wf, tgt) {
      return new CMS.Models.Cycle({
        workflow: wf,
        autogenerate: true,
        context: wf.context
      }).save();
    });
  },
  computed_errors: can.compute(function() {
    var errors = null;
    if(!this.attr("assignee")) {
      errors = { assignee: "Must be defined" };
    }
    if(!this.attr("end_date")) {
      errors = $.extend(errors, { end_date : "Must be defined" });
    }
    return errors;
  })
});

GGRC.Controllers.Modals("GGRC.Controllers.ApprovalWorkflow", {
  defaults : {
    original_object : null,
    new_object_form: true,
    model: CMS.ModelHelpers.ApprovalWorkflow,
    modal_title: "Submit for review",
    content_view: GGRC.mustache_path + "/wf_objects/approval_modal_content.mustache",
    button_view : GGRC.Controllers.Modals.BUTTON_VIEW_SAVE_CANCEL
  }
}, {
  init : function() {
    this.options.button_view = GGRC.Controllers.Modals.BUTTON_VIEW_SAVE_CANCEL;
    this._super.apply(this, arguments);
    this.options.attr("instance", new CMS.ModelHelpers.ApprovalWorkflow({
      original_object : this.options.instance
    }));
  },

});

GGRC.register_modal_hook("approvalform", function($target, $trigger, option) {
  var instance,
      object_params = JSON.parse($trigger.attr('data-object-params') || "{}");

  if($trigger.attr('data-object-id') === "page") {
    instance = GGRC.page_instance();
  } else {
    instance = CMS.Models.get_instance(
      $trigger.data('object-singular'),
      $trigger.attr('data-object-id')
    );
  }

  $target
  .modal_form(option, $trigger)
  .ggrc_controllers_approval_workflow({
    object_params : object_params,
    current_user : GGRC.current_user,
    instance : instance
  });
});

})(this.can, this.can.$, this.GGRC, this.CMS);
