/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import SavedSearch from '../../../models/service-models/saved-search';

export default can.Component.extend({
  tag: 'saved-search-wrapper',
  leakScope: true,
  viewModel: can.Map.extend({
    define: {
      objectType: {
        set(newValue, setValue) {
          setValue(newValue);

          this.loadSavedSearches();
        },
      },
    },
    searches: [],
    filterItems: [],
    applySearch({search}) {
      const query = JSON.parse(search.query)[0];
      const filters = query.filters;
      console.log(filters);
    },
    init() {
      this.loadSavedSearches();
    },
    loadSavedSearches() {
      return SavedSearch.findByType(this.attr('objectType'))
        .then(({values}) => {
          const searches = values.map((value) => new SavedSearch(value));
          this.attr('searches', searches);
        });
    },
  }),
});
