/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import workflowHelpers from './workflow-helpers';
import {
  initCounts,
} from '../../plugins/utils/current-page-utils';
import Permission from '../../permission';

const viewModel = can.Map.extend({
  taskGroupAmount: 0,
  instance: {},
  waiting: true,
  can_activate: false,
  _can_activate_def: function () {
    let self = this;
    const workflow = this.attr('instance');

    self.attr('waiting', true);
    $.when(
      workflow.refresh_all('task_groups', 'task_group_objects'),
      workflow.refresh_all('task_groups', 'task_group_tasks')
    )
    .always(function () {
      self.attr('waiting', false);
    })
    .done(function () {
      let taskGroups = workflow.task_groups.reify();
      let canActivate = taskGroups.length;

      taskGroups.each(function (taskGroup) {
        if (!taskGroup.task_group_tasks.length) {
          canActivate = false;
        }
      });
      self.attr('can_activate', canActivate);
    })
    .fail(function (error) {
      console.warn('Workflow activate error', error.message);
    });
  },
  _handle_refresh: function (model) {
    let models = ['TaskGroupTask', 'TaskGroupObject'];
    if (models.indexOf(model.shortName) > -1) {
      this._can_activate_def();
    }
  },
  async initWorkflow(workflow) {
    await workflow.refresh();
    workflow.attr({
      recurrences: true,
      status: 'Active',
    });
    return workflow.save();
  },
  async updateActiveCycleCounts(workflow) {
    const WorkflowExtension =
      _.find(GGRC.extensions, (extension) => extension.name === 'workflows');

    return initCounts([
      WorkflowExtension.countsMap.activeCycles,
    ], workflow.type, workflow.id);
  },
  redirectToFirstCycle(workflow) {
    const cycleStub = workflow.attr('cycles')[0];
    workflowHelpers.redirectToCycle(cycleStub);
  },
  async repeatOnHandler(workflow) {
    let result = Promise.resolve();
    this.attr('waiting', true);
    try {
      await this.initWorkflow(workflow);
      await Permission.refresh();
      await this.updateActiveCycleCounts(workflow);
      await workflow.refresh_all('task_groups', 'task_group_tasks');
      this.redirectToFirstCycle(workflow);
    } catch (err) {
      result = Promise.reject(err);
    } finally {
      this.attr('waiting', false);
    }

    return result;
  },
  async repeatOffHandler(workflow) {
    this.attr('waiting', true);
    try {
      await workflowHelpers.generateCycle(workflow);
      await workflow.refresh();
      await workflow.attr('status', 'Active').save();
    } catch (err) {
      return Promise.reject(err);
    } finally {
      this.attr('waiting', false);
    }
  },
  async activateWorkflow() {
    const workflow = this.attr('instance');
    try {
      if (workflow.unit !== null) {
        await this.repeatOnHandler(workflow);
      } else {
        await this.repeatOffHandler(workflow);
      }
    } catch (err) {
      // Do nothing
    }
  },
});

const events = {
  '{viewModel} taskGroupAmount'() {
    this.viewModel._can_activate_def();
  },
  '{can.Model.Cacheable} created': function (model) {
    this.viewModel._handle_refresh(model);
  },
  '{can.Model.Cacheable} destroyed': function (model) {
    this.viewModel._handle_refresh(model);
  },
  'button click': function () {
    this.viewModel.activateWorkflow();
  },
};

const init = function () {
  this.viewModel._can_activate_def();
};

export default can.Component.extend({
  tag: 'workflow-activate',
  init,
  viewModel,
  events,
});
