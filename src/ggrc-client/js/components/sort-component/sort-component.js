/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
export default CanComponent.extend({
  tag: 'sort-component',
  leakScope: true,
  viewModel: CanMap.extend({
    sortedItems: [],
    items: [],
    sort() {
      const items = this.attr('items');
      const sortedItems = items.sort();
      this.attr('sortedItems', sortedItems);
    },
  }),
  events: {
    '{viewModel.items} change'() {
      this.viewModel.sort();
    },
    init() {
      this.viewModel.sort();
    },
  },
});
