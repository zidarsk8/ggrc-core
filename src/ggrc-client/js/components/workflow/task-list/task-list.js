/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './templates/task-list.mustache';
import Pagination from '../../base-objects/pagination';
import Permission from '../../../permission';

const viewModel = can.Map.extend({
  /**
   * A model name. Each item within the task list
   * will have this model name.
   */
  relatedItemsType: 'TaskGroupTask',
}, {
  define: {
    paging: {
      value() {
        return new Pagination({pageSizeSelect: [5, 10, 15]});
      },
    },
    showCreateTaskButton: {
      get() {
        const workflow = this.attr('workflow');
        return (
          Permission.is_allowed_for('update', this.attr('baseInstance')) &&
          workflow && workflow.attr('status') !== 'Inactive'
        );
      },
    },
    relatedItemsType: {
      get() {
        return this.constructor.relatedItemsType;
      },
    },
  },
  initialOrderBy: 'created_at',
  gridSpinner: 'grid-spinner',
  items: [],
  baseInstance: null,
  workflow: null,
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
  updatePagingAfterDestroy() {
    const current = this.attr('paging.current');
    const isEmptyPage = (
      current > 1 &&
      this.attr('items').length === 1
    );

    if (isEmptyPage) {
      // go to previous page
      this.attr('paging.current', current - 1);
    } else {
      // update current page
      this.attr('baseInstance').dispatch('refreshInstance');
    }
  },
});

const events = {
  [`{CMS.Models.${viewModel.relatedItemsType}} destroyed`](
    model, event, instance
  ) {
    if (instance instanceof CMS.Models[viewModel.relatedItemsType]) {
      this.viewModel.updatePagingAfterDestroy();
    }
  },
  [`{CMS.Models.${viewModel.relatedItemsType}} created`](
    model, event, instance
  ) {
    if (instance instanceof CMS.Models[viewModel.relatedItemsType]) {
      this.viewModel.updatePagingAfterCreate();
    }
  },
};

export default can.Component.extend({
  tag: 'task-list',
  template,
  viewModel,
  events,
});
