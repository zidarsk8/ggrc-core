/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import SavedSearch from '../../../models/service-models/saved-search';
import {notifier} from '../../../plugins/utils/notifiers-utils';
import Pagination from '../../base-objects/pagination';
import {isObjectContextPage, isAllObjects} from '../../../plugins/utils/current-page-utils';
import {
  parseFilterJson,
  filterParentItems,
} from '../../../plugins/utils/advanced-search-utils';

export default can.Component.extend({
  tag: 'saved-search-wrapper',
  leakScope: true,
  viewModel: can.Map.extend({
    define: {
      isGlobalSearch: {
        value() {
          return !this.attr('advancedSearch');
        },
      },
      isShowSavedSearch: {
        value() {
          return this.attr('isGlobalSearch')
            || isObjectContextPage() || isAllObjects();
        },
      },
      objectType: {
        set(newValue, setValue) {
          setValue(newValue);

          if (this.attr('isShowSavedSearch')) {
            this.loadSavedSearches();
          }
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
    searchType: '',
    filtersToApply: null,
    advancedSearch: null,
    applySearch({search}) {
      try {
        const filter = parseFilterJson(search.filters);
        const advancedSearch = this.attr('advancedSearch');

        const parent = advancedSearch && advancedSearch.attr('parent');
        if (parent && filter.parentItems) {
          filter.parentItems = filterParentItems(parent, filter.parentItems);
        }

        if (advancedSearch) {
          advancedSearch.attr('filterItems', filter.filterItems);
          advancedSearch.attr('mappingItems', filter.mappingItems);
          advancedSearch.attr('parentItems', filter.parentItems);
        } else {
          this.attr('filtersToApply', {
            filterItems: filter.filterItems,
            mappingItems: filter.mappingItems,
            statusItem: filter.statusItem,
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
      const searchType = this.attr('searchType');

      return SavedSearch.findBy(type, searchType, paging)
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
