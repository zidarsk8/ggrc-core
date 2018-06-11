/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import workflowHelpers from '../../plugins/utils/workflow-utils';
import {
  initCounts,
} from '../../plugins/utils/current-page-utils';
import Permission from '../../permission';

const viewModel = can.Map.extend({
  instance: {},
  waiting: false,
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

export default can.Component.extend({
  tag: 'workflow-activate',
  viewModel,
});
