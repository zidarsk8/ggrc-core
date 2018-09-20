/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Cacheable from '../cacheable';
import '../mixins/is-overdue';
import Stub from '../stub';

export default Cacheable('CMS.Models.CycleTaskGroup', {
  root_object: 'cycle_task_group',
  root_collection: 'cycle_task_groups',
  category: 'workflow',
  findAll: 'GET /api/cycle_task_groups',
  findOne: 'GET /api/cycle_task_groups/{id}',
  create: 'POST /api/cycle_task_groups',
  update: 'PUT /api/cycle_task_groups/{id}',
  destroy: 'DELETE /api/cycle_task_groups/{id}',
  mixins: ['isOverdue'],
  attributes: {
    cycle: Stub,
    task_group: Stub,
    cycle_task_group_tasks: Stub.List,
    modified_by: Stub,
    context: Stub,
  },

  tree_view_options: {
    draw_children: true,
  },

  init: function () {
    this._super(...arguments);
    this.validateNonBlank('contact');
    this.validateContact(['_transient.contact', 'contact']);
  },
}, {});
