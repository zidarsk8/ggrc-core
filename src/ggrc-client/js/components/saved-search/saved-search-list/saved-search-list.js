/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './saved-search-list.stache';

export default can.Component.extend({
  tag: 'saved-search-list',
  template: can.stache(template),
  leakScope: false,
  viewModel: can.Map.extend({
    objectName: '',
    searches: [],
    applySearch(search) {
      if (this.attr('disabled')) {
        return;
      }
      this.dispatch({
        type: 'applySearch',
        search,
      });
    },
    removeSearch(search, event) {
      event.stopPropagation();
      search.attr('disabled', true);

      search.destroy().then(() => {
        this.dispatch('removed');
      });
    },
  }),
});
