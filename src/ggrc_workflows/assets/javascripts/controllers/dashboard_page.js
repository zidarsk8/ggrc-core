/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/

;(function(CMS, GGRC, can, $) {

  function init_my_tasks() {
    //To get the tasks only for the current person/current cycle
    var loader = GGRC.page_instance().get_binding("assigned_tasks");
    if(loader) {
      this.display_tasks(loader);
    }
    return 0;
  }

  function display_tasks(loader) {
    var self = this,
        task_data = {};

    loader.refresh_instances().then(function(tasks) {
      self.attr('task_count', tasks.length);
      task_data.list = tasks;
      task_data.filtered_list = tasks;
      self.attr('task_data', task_data);
      self.attr('tasks_loaded', true);
    });
    return 0;
  }

  function load_my_audit_requests() {
    var self = this,
        loader;

    //Get the audits only for the current person
    loader = GGRC.page_instance().get_binding("open_audit_requests");
    if (loader) {
      loader.refresh_instances().then(function(audits) {
        self.attr('audit_requests_count', audits.length);
        self.attr('audit_requests_data', {list: audits});
      });
    }
  }

  function load_task_with_history() {
    //load assigned tasks and history
    var loader = GGRC.page_instance().get_binding("assigned_tasks_with_history");
    if(loader) {
      this.display_tasks(loader);
    }
    return 0;
  }

  function autocomplete_select(el, ev, ui) {
    if (!ui) {
      return;
    }
    setTimeout(function() {
      if (ui.item.title) {
        el.val(ui.item.title, ui.item);
      } else {
        el.val(ui.item.name ? ui.item.name : ui.item.email, ui.item);
      }
      el.trigger('change');
    }, 0);
  }

  function is_overdue_task(task) {
    var end_date = new Date(task.instance.end_date || null),
        today = new Date();

    //Any task that is not finished or verified are subject to overdue
    if (task.instance.status === "Finished" || task.instance.status === "Verified")
      return false;
    else if (end_date.getTime() < today.getTime())
      return true;
  }

  function filter_task_data() {
    var list = this.task_data.list, //original list of data
        i,
        task_data = {},
        list1 = [], //list filtered by status
        my_list = [],
        list2 = [], //list filtered by object or workflow
        filtered_list = [], //final filtered list
        filter = this.task_filter,
        status_flag = false,
        cycle,
        obj,
        obj_flag = false;

    //Filter by status first
    if (filter.overdue === 1) {
      status_flag = true;
      for (i = 0; i < list.length; i++) {
        if (this.is_overdue_task(list[i]))
          list1.push(list[i]);
      }
    } else if (filter.status === "Verified"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].instance.status === "Verified")
          list1.push(list[i]);
    } else if (filter.status === "Finished"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].instance.status === "Finished")
          list1.push(list[i]);
    } else if (filter.status === "InProgress"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].instance.status === "InProgress")
          list1.push(list[i]);
    } else if (filter.status === "Assigned"){
      status_flag = true;
      for (i = 0; i < list.length; i++)
        if (list[i].instance.status === "Assigned")
          list1.push(list[i]);
    }

    //Now filter by object and workflow
    if (status_flag){
        my_list = list1;
    } else {
        my_list = list;
    }

    if (filter.workflow !== '' && filter.object !== '') {
      obj_flag = true;
      for (i = 0; i < my_list.length; i++) {
        cycle = my_list[i].instance.cycle.reify();
        obj = my_list[i].instance.cycle_task_group_object;
        if (filter.workflow === cycle.workflow.title && filter.object === obj.object.title)
          list2.push(my_list[i]);
      }

    } else if (filter.workflow !== '') {
      obj_flag = true;
      for (i = 0; i < my_list.length; i++) {
        cycle = my_list[i].instance.cycle.reify();
        if (filter.workflow === cycle.title)
          list2.push(my_list[i]);
      }
    } else if (filter.object !== '') {
      obj_flag = true;
      for (i = 0; i < my_list.length; i++) {
        if (my_list[i].instance.cycle_task_group_object) {
          obj = my_list[i].instance.cycle_task_group_object.reify();
          if (filter.object === obj.title)
            list2.push(my_list[i]);
        }
      }
    }

    if (obj_flag) {
      filtered_list = list2;
    } else if (status_flag) {
      filtered_list = list1;
    } else {
      filtered_list = list;
    }

    task_data.list = list;
    task_data.filtered_list = filtered_list;
    this.attr('task_data', task_data);
  }

  can.Component.extend({
    tag: "dashboard-widgets",
    template: "<content/>",
    scope: {
      initial_wf_size: 5,
      workflow_view: GGRC.mustache_path + "/dashboard/info/workflow_progress.mustache",
      workflow_data: {},
      workflow_count: 0,
      workflow_show_all: false,
      task_view: GGRC.mustache_path + "/dashboard/info/my_tasks.mustache",
      task_data: {},
      task_count: 0,
      audit_requests_view: GGRC.mustache_path + "/dashboard/info/my_audit_requests.mustache",
      audit_requests_data: {},
      audit_requests_count: 0,
      task_filter: {
        status: '',     //initialy any task should be displayed
        object: '',     // not filtered by any object, object = empty string
        workflow: '',   // not filtered by workflow, workflow = empty string
        overdue: 0      // not filtered by overdue status
      },
      load_my_audit_requests: load_my_audit_requests,
      load_task_with_history: load_task_with_history,
      autocomplete_select: autocomplete_select,
      is_overdue_task: is_overdue_task,
      filter_task_data: filter_task_data,
      display_tasks: display_tasks,
      init_my_tasks: init_my_tasks,
    },
    events: {
      // Click action to show all workflows
      "a.workflow-trigger.show-all click" : function(el, ev) {
        this.scope.workflow_data.attr('list', this.scope.workflow_data.cur_wfs);

        el.text('Show top 5 workflows');
        el.removeClass('show-all');
        el.addClass('show-5');

        ev.stopPropagation();
      },
      //Show onlt top 5 workflows
      "a.workflow-trigger.show-5 click" : function(el, ev) {
        this.scope.workflow_data.attr('list', this.scope.workflow_data.cur_wfs5);

        el.text('Show all my workflows');
        el.removeClass('show-5');
        el.addClass('show-all');

        ev.stopPropagation();
      },
      // Show Audits
      "li.audit-tab click" : function(el, ev) {
        this.element.find('li.task-tab').removeClass('active');
        this.element.find('ul.inline-task-filter').hide();
        this.element.find('ul.task-tree').hide();
        this.element.find('li.workflow-tab').removeClass('active');
        this.element.find('.workflow-wrap-main').hide();

        el.addClass('active');

        if (!this.scope.show_audit) {
          this.scope.attr('show_audit', true);
          this.scope.load_my_audit_requests();
        } else {
          this.element.find('ul.audit-tree').show();
        }
        ev.stopPropagation();
      },
      // Show Workflows
      "li.workflow-tab click" : function(el, ev) {
        this.element.find('li.task-tab').removeClass('active');
        this.element.find('ul.inline-task-filter').hide();
        this.element.find('ul.task-tree').hide();
        this.element.find('li.audit-tab').removeClass('active');
        this.element.find('ul.audit-tree').hide();

        el.addClass('active');
        this.element.find('.workflow-wrap-main').show();
        ev.stopPropagation();
      },
      // Show Tasks
      "li.task-tab click" : function(el, ev) {
        this.element.find('li.audit-tab').removeClass('active');
        this.element.find('ul.audit-tree').hide();
        this.element.find('li.workflow-tab').removeClass('active');
        this.element.find('.workflow-wrap-main').hide();

        el.addClass('active');
        this.element.find('ul.inline-task-filter').show();
        this.element.find('ul.task-tree').show();
        ev.stopPropagation();
      },
      "input[data-lookup] focus" : function(el, ev) {
        $.cms_autocomplete.call(this, el);
      },
      "input[type=text], input[type=checkbox].filter-overdue, select change" : function(el, ev) {
        var filter_task_data = {};
        filter_task_data.list = [];
        var filters = {};
        //find all the filters, filter the existing task_data, don't need to go to the server
        //show the data
        var obj = this.element.find('input[name="object"]').val();
        var wf = this.element.find('input[name="workflow"]').val();
        var status = this.element.find('select[name="status"]').val();
        var overdue = this.element.find('input[type=checkbox].filter-overdue:checked').length;

        //set up task filter
        this.scope.task_filter.status = status;
        this.scope.task_filter.object = obj;
        this.scope.task_filter.workflow = wf;
        this.scope.task_filter.overdue = overdue;

        //filter task_data
        this.scope.filter_task_data();

        this.scope.attr('task_count', this.scope.task_data.filtered_list.length);

        ev.stopPropagation();
      },
      "input[type=checkbox].show-history change" : function(el, ev) {
        if (this.element.find('input[type=checkbox].show-history:checked').length === 1) {
          this.scope.load_task_with_history();
        } else {
          this.scope.init_my_tasks();
        }
        ev.stopPropagation();
      }
    },
    init: function() {
      this.init_my_workflows();
      this.scope.init_my_tasks();
      this.init_audit_requests_count();
    },
    init_my_workflows: function() {
      var self = this,
          my_view = this.scope.workflow_view,
          workflow_data = {},
          wfs,              // list of all workflows
          cur_wfs,          // list of workflows with current cycles
          cur_wfs5;         // list of top 5 workflows with current cycle

      if (!GGRC.current_user) {
        return;
      }
      GGRC.Models.Search.search_for_types('', ['Workflow'], {contact_id: GGRC.current_user.id})
      .then(function(result_set){
          var wf_data = result_set.getResultsForType('Workflow');
          var refresh_queue = new RefreshQueue();
          refresh_queue.enqueue(wf_data);
          return refresh_queue.trigger();
      }).then(function(options){
          wfs = options;

          return $.when.apply($, can.map(options, function(wf){
            return self.update_tasks_for_workflow(wf);
          }));
      }).then(function(){
        if(wfs.length > 0){
          //Filter workflows with a current cycle
          cur_wfs = self.filter_current_workflows(wfs);
          self.scope.attr('workflow_count', cur_wfs.length);
          //Sort the workflows in accending order by first_end_date
          cur_wfs.sort(self.sort_by_end_date);
          workflow_data.cur_wfs = cur_wfs;

          if (cur_wfs.length > self.scope.initial_wf_size) {
            cur_wfs5 = cur_wfs.slice(0, self.scope.initial_wf_size);
            self.scope.attr('workflow_show_all', true);
          } else {
            cur_wfs5 = cur_wfs;
            self.scope.attr('workflow_show_all', false);
          }

          workflow_data.cur_wfs5 = cur_wfs5;
          workflow_data.list = cur_wfs5;
          self.scope.attr('workflow_data', workflow_data);
        }
      });

      return 0;
    },
    init_audit_requests_count: function() {
      var self = this;

      if (!GGRC.current_user) {
        return 0;
      }

      GGRC.page_instance().get_binding("open_audit_requests").refresh_count()
        .then(function(result) {
          self.scope.attr('audit_requests_count', result());
      });
      return 0;
    },
    update_tasks_for_workflow: function(workflow){
      var self = this,
          dfd = $.Deferred(),
          task_count = 0,
          finished = 0,
          in_progress = 0,
          declined = 0,
          verified = 0,
          assigned = 0,
          over_due = 0,
          today = new Date(),
          first_end_date,
          task_data = {};

        workflow.get_binding('current_all_tasks').refresh_instances().then(function(d){
          var mydata = d;
          task_count = mydata.length;
          for(var i = 0; i < task_count; i++){
            var data = mydata[i].instance,
                end_date = new Date(data.end_date || null);

            //Calculate first_end_date for the workflow / earliest end for all the tasks in a workflow
            if (i === 0)
              first_end_date = end_date;
            else if (end_date.getTime() < first_end_date.getTime())
              first_end_date = end_date;

            //Any task not verified is subject to overdue
            if (data.status === 'Verified')
              verified++;
            else {
              if (end_date.getTime() < today.getTime()) {
                over_due++;
                $('dashboard-errors').control().scope.attr('error_msg', 'Some tasks are overdue!');
              }
              else if (data.status === 'Finished')
                finished++;
              else if (data.status === 'InProgress')
                in_progress++;
              else if (data.status === 'Declined')
                declined++;
              else
                assigned++;
            }
          }
          //Update Task_data object for workflow and Calculate %
          if (task_count > 0) {
            task_data.task_count = task_count;
            task_data.finished = finished;
            task_data.finished_percentage = ((finished * 100) / task_count).toFixed(2); //precision up to 2 decimal points
            task_data.in_progress = in_progress;
            task_data.in_progress_percentage = ((in_progress * 100) / task_count).toFixed(2);
            task_data.verified = verified;
            task_data.verified_percentage = ((verified * 100) / task_count).toFixed(2);
            task_data.declined = declined;
            task_data.declined_percentage = ((declined * 100) / task_count).toFixed(2);
            task_data.over_due = over_due;
            task_data.over_due_percentage = ((over_due * 100) / task_count).toFixed(2);
            task_data.assigned = assigned;
            task_data.assigned_percentage = ((assigned * 100) / task_count).toFixed(2);
            task_data.first_end_dateD = first_end_date;
            task_data.first_end_date = first_end_date.toLocaleDateString();
            //calculate days left for first_end_date
            if(today.getTime() >= first_end_date.getTime())
              task_data.days_left_for_first_task = 0;
            else {
              var time_interval = first_end_date.getTime() - today.getTime();
              var day_in_milli_secs = 24 * 60 * 60 * 1000;
              task_data.days_left_for_first_task = Math.floor(time_interval/day_in_milli_secs);
            }

            //set overdue flag
            task_data.over_due_flag = over_due ? true : false;
          }

          workflow.attr('task_data', new can.Map(task_data));
          dfd.resolve();
        });

        return dfd;
    },
    /*
      filter_current_workflows filters the workflows with current tasks in a
      new array and returns the new array.
      filter_current_workflows should be called after update_tasks_for_workflow.
      It looks at the task_data.task_count for each workflow
      For workflow with current tasks, task_data.task_count must be > 0;
    */
    filter_current_workflows: function(workflows){
      var filtered_wfs = [];

      can.each(workflows, function(item){
        if (item.task_data) {
          if (item.task_data.task_count > 0)
            filtered_wfs.push(item);
        }
      });
      return filtered_wfs;
    },
    /*
      sort_by_end_date sorts workflows in assending order with respect to task_data.first_end_date
      This should be called with workflows with current tasks.
    */
    sort_by_end_date: function(a, b) {
        return (a.task_data.first_end_dateD.getTime() - b.task_data.first_end_dateD.getTime());
    }

  });

  can.Component.extend({
    tag: "dashboard-errors",
    template: "<content/>",
    scope: {
      error_msg: '',
    }
  });

})(this.CMS, this.GGRC, this.can, this.can.$);
