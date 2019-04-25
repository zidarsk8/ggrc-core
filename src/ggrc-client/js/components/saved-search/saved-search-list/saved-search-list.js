/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './saved-search-list.stache';
import SavedSearch from '../../../models/service-models/saved-search';

export default can.Component.extend({
  tag: 'saved-search-list',
  template: can.stache(template),
  leakScope: false,
  viewModel: can.Map.extend({
    objectName: '',
    searches: [],
    init() {
      SavedSearch.findByType(this.attr('objectName')).then((data) => {
        this.attr('searches', data.values);
      });
    },
    removeSearch(search) {
      search.destroy();
    },
  }),
});
