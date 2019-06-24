/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanComponent from 'can-component';
import template from './document-object-list-item.stache';
import '../spinner-component/spinner-component';

/**
 * Simple component to show Document-like Objects
 */
export default CanComponent.extend({
  tag: 'document-object-list-item',
  view: can.stache(template),
  leakScope: true,
  viewModel: can.Map.extend({
    instance: {},
    define: {
      itemData: {
        get() {
          return this.attr('instance');
        },
      },
      itemTitle: {
        get() {
          return this.attr('itemData.title') || this.attr('itemData.link');
        },
      },
      itemCreationDate: {
        get() {
          return this.attr('itemData.created_at');
        },
      },
      itemStatus: {
        get() {
          return this.attr('itemData.status');
        },
      },
      isItemValid: {
        get() {
          return this.attr('itemStatus').toLowerCase() !== 'deprecated';
        },
      },
    },
  }),
});
