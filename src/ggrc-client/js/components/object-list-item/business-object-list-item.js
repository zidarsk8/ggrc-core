/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './business-object-list-item.mustache';

let tag = 'business-object-list-item';
/**
 * Mapped objects item view component
 */
export default can.Component.extend({
  tag,
  template,
  viewModel: {
    instance: {},
    define: {
      type: {
        type: String,
      },
      isSnapshot: {
        get() {
          return this.attr('instance.type') === 'Snapshot';
        },
      },
      iconCls: {
        get() {
          const objectType = !this.attr('isSnapshot') ?
            this.attr('instance.type') :
            this.attr('instance.child_type');
          const model = CMS.Models[objectType];
          return `fa-${model.table_singular}`;
        },
      },
      itemData: {
        get() {
          return !this.attr('isSnapshot') ?
            this.attr('instance') :
            this.attr('instance.revision.content');
        },
      },
      itemTitle: {
        get() {
          return this.attr('itemData.title') ||
            this.attr('itemData.description_inline') ||
            this.attr('itemData.name') ||
            this.attr('itemData.email') ||
            '<span class="empty-message">None</span>';
        },
      },
    },
  },
});
