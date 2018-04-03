/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './templates/task-list.mustache';

const viewModel = can.Map.extend({
  items: [],
});

const events = {
  inserted(el) {
    $(el).sortable({
      items: '.task_group_tasks__list-item',
      handle: '.drag',
    });
  },
};

export default can.Component.extend({
  tag: 'task-list',
  template,
  viewModel,
  events,
});
