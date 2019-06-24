/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
import '../../info-pin-buttons/info-pin-buttons';
import '../task-group-clone';
import '../task-list/task-list';
import '../task-group-objects/task-group-objects';
import template from './templates/task-group.stache';
import Permission from '../../../permission';

const viewModel = CanMap.extend({
  define: {
    canEdit: {
      get() {
        return (
          Permission.is_allowed_for('update', this.attr('instance')) &&
          this.attr('workflow.status') !== 'Inactive'
        );
      },
    },
  },
  instance: null,
  workflow: null,
  async loadWorkflow() {
    const instance = this.attr('instance');
    const workflow = await instance.refresh_all('workflow');
    this.attr('workflow', workflow);
  },
});


const init = function () {
  this.viewModel.loadWorkflow();
};

export default CanComponent.extend({
  tag: 'task-group',
  view: can.stache(template),
  leakScope: true,
  viewModel,
  init,
});
