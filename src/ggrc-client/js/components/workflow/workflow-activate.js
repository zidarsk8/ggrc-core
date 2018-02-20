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
  async handleWorkflowActivation() {
    const workflow = this.attr('instance');
    this.attr('waiting', true);
    try {
      await Promise.all([
        workflow.refresh_all('task_groups', 'task_group_objects'),
        workflow.refresh_all('task_groups', 'task_group_tasks'),
      ]);
      this.attr('can_activate', this.canActivateWorkflow(workflow));
    } catch (error) {
      console.warn('Workflow activate error', error.message); // eslint-disable-line
    } finally {
      this.attr('waiting', false);
    }
  },
  canActivateWorkflow(workflow) {
    const taskGroups = workflow.task_groups.reify();
    const hasTaskGroups = taskGroups.length > 0;
    const nonEmptyTaskGroupTasks = _.all(
      taskGroups,
      'task_group_tasks.length'
    );
    return hasTaskGroups && nonEmptyTaskGroupTasks;
  },
  handleModelsActivation(model) {
    let models = ['TaskGroupTask', 'TaskGroupObject'];
    if (models.indexOf(model.shortName) > -1) {
      this.handleWorkflowActivation();
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
    this.viewModel.handleWorkflowActivation();
  },
  '{can.Model.Cacheable} created'(model) {
    this.viewModel.handleModelsActivation(model);
  },
  '{can.Model.Cacheable} destroyed'(model) {
    this.viewModel.handleModelsActivation(model);
  },
};

const init = function () {
  this.viewModel.handleWorkflowActivation();
};

export default can.Component.extend({
  tag: 'workflow-activate',
  init,
  viewModel,
  events,
});
