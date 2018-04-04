/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import '../../info-pin-buttons/info-pin-buttons';
import '../taskgroup_clone';
import '../task-list/task-list';

import template from './templates/task-group.mustache';

const viewModel = can.Map.extend({
  instance: null,
  workflow: null,
  options: null,
  taskGroupTasks: [],
  async loadTaskGroupTasks() {
    const instance = this.attr('instance');
    const taskGroupTasks = await instance.refresh_all('task_group_tasks');
    this.attr('taskGroupTasks').replace(taskGroupTasks);
  },
  async loadWorkflow() {
    const instance = this.attr('instance');
    const workflow = await instance.refresh_all('workflow');
    this.attr('workflow', workflow);
  },
});

const events = {
  async '{CMS.Models.TaskGroupTask} created'() {
    // After TGT creation, TG will have an updated
    // list with TGTs. Because of that, TG should be refreshed.
    await this.viewModel.instance.refresh();
    this.viewModel.loadTaskGroupTasks();
  },
};

const init = function () {
  this.viewModel.loadTaskGroupTasks();
  this.viewModel.loadWorkflow();
};

export default can.Component.extend({
  tag: 'task-group',
  template,
  viewModel,
  events,
  init,
});
