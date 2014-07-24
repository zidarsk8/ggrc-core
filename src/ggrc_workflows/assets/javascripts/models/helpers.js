/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

;(function(can, $, CMS) {

can.Observe("CMS.ModelHelpers.CycleTask", {
  findInCacheById : function() { return null; },
}, {
  init : function() {
    this.attr("owners", new CMS.Models.Person.List(this.owners));
  },
  save : function() {
    var that = this;
    return new CMS.Models.Task(this._data).save().then(function(task) {
      return new CMS.Models.TaskGroupTask({
        task_group: that.task_group,
        task: task,
        sort_index: Number.MAX_SAFE_INTEGER / 2,
        contact: that.contact,
        context: that.context
      }).save();
    }).then(function(task_group_task) {
      return new CMS.Models.CycleTaskGroupObjectTask({
        cycle: that.cycle,
        start_date: that.cycle.reify().start_date,
        end_date: that.cycle.reify().end_date,
        task_group_task: task_group_task,
        cycle_task_group_object: that.cycle_task_group_object,
        sort_index: that.sort_index,
        title: that.title,
        description: that.description,
        status: "Assigned",
        contact: that.contact,
        context: that.context
      }).save();
    });
  },
  computed_errors: can.compute(function() {
    var errors = null;
    if(!this.attr("title")) {
      errors = { title: "Must be defined" };
    }
    return errors;
  })
});


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
          sort_index: (Number.MAX_SAFE_INTEGER / 2).toString(10),
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

})(this.can, this.can.$, this.CMS);
