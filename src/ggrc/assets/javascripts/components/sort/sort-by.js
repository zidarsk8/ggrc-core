/*
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

const tag = 'sort-by';

export default can.Component.extend({
  tag,
  viewModel: {
    define: {
      sortedItems: {
        get() {
          const propName = this.attr('propertyName');
          const items = this.attr('items');
          if (!items || !items.length || !propName) {
            return items;
          }

          return _.sortBy(items, propName);
        },
      },
    },
    items: [],
    propertyName: '@',
  },
});
