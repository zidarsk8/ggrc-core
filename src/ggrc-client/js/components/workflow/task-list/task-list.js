/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './templates/task-list.mustache';
import Pagination from '../../base-objects/pagination';

const viewModel = can.Map.extend({
  define: {
    paging: {
      value() {
        return new Pagination({pageSizeSelect: [5, 10, 15]});
      },
    },
  },
  relatedItemsType: 'TaskGroupTask',
  initialOrderBy: 'created_at',
  gridSpinner: 'grid-spinner',
  items: [],
  baseInstance: null,
  updatePagingAfterCreate() {
    if (this.attr('paging.current') !== 1) {
      // items will be reloaded, because the current
      // value will be changed to first page
      this.attr('paging.current', 1);
    } else {
      // reload items manually, because CanJs does not
      // trigger "change" event, when we try to set first page
      // (we are already on first page)
      this.attr('baseInstance').dispatch('refreshInstance');
    }
  },
});

const events = {
  '{CMS.Models.TaskGroupTask} created'() {
    this.viewModel.updatePagingAfterCreate();
  },
};

export default can.Component.extend({
  tag: 'task-list',
  template,
  viewModel,
  events,
});
