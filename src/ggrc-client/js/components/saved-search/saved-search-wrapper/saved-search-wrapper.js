/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import SavedSearch from '../../../models/service-models/saved-search';
import {notifier} from '../../../plugins/utils/notifiers-utils';
import Pagination from '../../base-objects/pagination';

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
      searchesPaging: {
        value() {
          return new Pagination({
            pageSize: 10, pageSizeSelect: [10],
          });
        },
      },
      isPagingShown: {
        get() {
          const total = this.attr('searchesPaging.total');
          const pageSize = this.attr('searchesPaging.pageSize');

          return total > pageSize;
        },
      },
    },
    searches: [],
    filtersToApply: null,
    advancedSearch: null,
    init() {
      this.loadSavedSearches();
    },
    applySearch({search}) {
      try {
        let {
          filterItems,
          mappingItems,
          statusItem,
          parentItems,
        } = JSON.parse(search.filters);

        const advancedSearch = this.attr('advancedSearch');

        const parent = advancedSearch && advancedSearch.attr('parent');
        if (parent && parentItems) {
          parentItems = parentItems.filter(
            (item) => item.value.id !== parent.value.id
              || item.value.type !== parent.value.type);
        }

        if (advancedSearch) {
          advancedSearch.attr('filterItems', filterItems);
          advancedSearch.attr('mappingItems', mappingItems);
          advancedSearch.attr('parentItems', parentItems);
        } else {
          this.attr('filtersToApply', {
            filterItems,
            mappingItems,
            statusItem,
          });
        }
      } catch (e) {
        notifier('error',
          `"${search.name}" is broken somehow. Sorry for any inconvenience.`);
      }
    },
    loadSavedSearches() {
      const type = this.attr('objectType');
      const paging = this.attr('searchesPaging');

      return SavedSearch.findByType(type, paging)
        .then(({total, values}) => {
          this.attr('searchesPaging.total', total);

          const searches = values.map((value) => new SavedSearch(value));
          this.attr('searches', searches);
        });
    },
  }),
  events: {
    '{viewModel.searchesPaging} current'() {
      this.viewModel.loadSavedSearches();
    },
  },
});
