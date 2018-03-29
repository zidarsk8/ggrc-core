/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import '../../info-pin-buttons/info-pin-buttons';
import '../taskgroup_clone';
import '../../sort_by_sort_index/sort_by_sort_index';

import template from './templates/task-group.mustache';

const viewModel = can.Map.extend({
  instance: null,
  options: null,
});

export default can.Component.extend({
  tag: 'task-group',
  template,
  viewModel,
});
