/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import RefreshQueue from '../models/refresh_queue';
import '../components/inline/people-with-role-inline-field';

export default can.Component.extend({
  tag: 'dashboard-widgets',
  template: '<content/>',
  scope: {
    initial_wf_size: 5,
    workflow_view: GGRC.mustache_path +
      '/dashboard/info/workflow_progress.mustache',
    workflow_data: {},
    workflow_count: 0,
    workflow_show_all: false,
  },
  events: {
    // Click action to show all workflows
    'a.workflow-trigger.show-all click'(el, ev) {
      this.scope.workflow_data.attr('list', this.scope.workflow_data.cur_wfs);

      el.text('Show top 5 workflows');
      el.removeClass('show-all');
      el.addClass('show-5');

      ev.stopPropagation();
    },
    // Show onlt top 5 workflows
    'a.workflow-trigger.show-5 click'(el, ev) {
      this.scope.workflow_data.attr('list', this.scope.workflow_data.cur_wfs5);

      el.text('Show all my workflows');
      el.removeClass('show-5');
      el.addClass('show-all');

      ev.stopPropagation();
    },

    // Show Workflows
    'li.workflow-tab click'(el, ev) {
      el.addClass('active');
      this.element.find('.workflow-wrap-main').show();
      ev.stopPropagation();
    },
  },
  init() {
    this.init_my_workflows();
  },
  init_my_workflows() {
    let self = this;
    let workflowData = {};
    let wfs; // list of all workflows
    let curWfs; // list of workflows with current cycles
    let curWfs5; // list of top 5 workflows with current cycle

    if (!GGRC.current_user) {
      return;
    }

    GGRC.Models.Search
      .search_for_types('', ['Workflow'], {contact_id: GGRC.current_user.id})
      .then(function (resultSet) {
        let wfData = resultSet.getResultsForType('Workflow');
        let refreshQueue = new RefreshQueue();
        refreshQueue.enqueue(wfData);
        return refreshQueue.trigger();
      }).then(function (options) {
        wfs = options;

        return $.when(...can.map(options, function (wf) {
          return self.update_tasks_for_workflow(wf);
        }));
      }).then(function () {
        if (wfs.length > 0) {
          // Filter workflows with a current cycle
          curWfs = self.filter_current_workflows(wfs);
          self.scope.attr('workflow_count', curWfs.length);
          // Sort the workflows in ascending order by first_end_date
          curWfs.sort(self.sort_by_end_date);
          workflowData.cur_wfs = curWfs;

          if (curWfs.length > self.scope.initial_wf_size) {
            curWfs5 = curWfs.slice(0, self.scope.initial_wf_size);
            self.scope.attr('workflow_show_all', true);
          } else {
            curWfs5 = curWfs;
            self.scope.attr('workflow_show_all', false);
          }

          workflowData.cur_wfs5 = curWfs5;
          workflowData.list = curWfs5;
          self.scope.attr('workflow_data', workflowData);
        }
      });

    return 0;
  },
  update_tasks_for_workflow(workflow) {
    let dfd = $.Deferred();
    let taskCount = 0;
    let finished = 0;
    let verified = 0;
    let overDue = 0;
    let today = new Date();
    let firstEndDate;
    let taskData = {};

    workflow.get_binding('current_all_tasks')
      .refresh_instances()
      .then((instData)=> {
        let mydata = instData;
        taskCount = mydata.length;
        for (let i = 0; i < taskCount; i++) {
          let data = mydata[i].instance;
          let endDate = new Date(data.end_date || null);

          // Calculate firstEndDate for the workflow / earliest end for all the tasks in a workflow
          if (i === 0) {
            firstEndDate = endDate;
          } else if (endDate.getTime() < firstEndDate.getTime()) {
            firstEndDate = endDate;
          }

          if (data.isOverdue) {
            overDue++;
            GGRC.Errors.notifier('error', 'Some tasks are overdue!');
          }
          switch (data.status) {
            case 'Verified':
              verified++;
              break;
            case 'Finished':
              finished++;
              break;
          }
        }
        // Update taskData object for workflow and Calculate %
        if (taskCount > 0) {
          taskData.task_count = taskCount;
          taskData.finished = finished;
          taskData.finished_percentage =
            ((finished * 100) / taskCount).toFixed(2);
          taskData.verified = verified;
          taskData.verified_percentage =
            ((verified * 100) / taskCount).toFixed(2);
          taskData.over_due = overDue;
          taskData.first_end_dateD = firstEndDate;
          taskData.first_end_date = firstEndDate.toLocaleDateString();
          // calculate days left for firstEndDate
          if (today.getTime() >= firstEndDate.getTime()) {
            taskData.days_left_for_first_task = 0;
          } else {
            let timeInterval = firstEndDate.getTime() - today.getTime();
            let dayInMillisecs = 24 * 60 * 60 * 1000;
            taskData.days_left_for_first_task =
              Math.floor(timeInterval/dayInMillisecs);
          }
          taskData.completed_percentage = workflow.is_verification_needed ?
            taskData.verified_percentage : taskData.finished_percentage;

          // set overdue flag
          taskData.over_due_flag = overDue ? true : false;
        }

        workflow.attr('task_data', new can.Map(taskData));
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
  filter_current_workflows(workflows) {
    let filteredWfs = [];

    can.each(workflows, function (item) {
      if (item.task_data) {
        if (item.task_data.task_count > 0) {
          filteredWfs.push(item);
        }
      }
    });
    return filteredWfs;
  },
  /*
    sort_by_end_date sorts workflows in assending order with respect to task_data.first_end_date
    This should be called with workflows with current tasks.
  */
  sort_by_end_date(a, b) {
    return (a.task_data.first_end_dateD.getTime() -
      b.task_data.first_end_dateD.getTime());
  },
});
