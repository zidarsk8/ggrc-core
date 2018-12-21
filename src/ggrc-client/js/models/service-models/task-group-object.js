/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Cacheable from '../cacheable';
import Stub from '../stub';

export default Cacheable('CMS.Models.TaskGroupObject', {
  root_object: 'task_group_object',
  root_collection: 'task_group_objects',
  attributes: {
    context: Stub,
    modified_by: Stub,
    task_group: Stub,
    object: Stub,
  },
  findAll: 'GET /api/task_group_objects',
  create: 'POST /api/task_group_objects',
  update: 'PUT /api/task_group_objects/{id}',
  destroy: 'DELETE /api/task_group_objects/{id}',
}, {});
