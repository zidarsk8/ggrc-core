/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './create-saved-search.stache';
import SavedSearch from '../../../models/service-models/saved-search';
import {handleAjaxError} from '../../../plugins/utils/errors-utils';

export default can.Component.extend({
  tag: 'create-saved-search',
  template: can.stache(template),
  leakScope: false,
  viewModel: can.Map.extend({
    filterItems: null,
    mappingItems: null,
    statusItem: null,
    parentItems: null,
    parent: null,
    type: null,
    searchName: '',
    objectType: '',
    isDisabled: false,
    getFilters() {
      const filterItems = this.attr('filterItems') &&
        this.attr('filterItems').serialize();
      const mappingItems = this.attr('mappingItems') &&
        this.attr('mappingItems').serialize();
      const statusItem = this.attr('statusItem') &&
        this.attr('statusItem').serialize();

      let parentItems = this.attr('parentItems') &&
        this.attr('parentItems').serialize();
      let parent = this.attr('parent');
      if (parent) {
        parent = parent.serialize();
        if (parentItems) {
          parentItems.push(parent);
        } else {
          parentItems = [parent];
        }
      }

      return {
        filterItems,
        mappingItems,
        statusItem,
        parentItems,
      };
    },
    saveSearch() {
      if (this.attr('isDisabled')) {
        return;
      }

      const filters = this.getFilters();
      const savedSearch = new SavedSearch({
        name: this.attr('searchName'),
        search_type: this.attr('type'),
        object_type: this.attr('objectType'),
        filters,
      });

      this.attr('isDisabled', true);
      return savedSearch.save().then(() => {
        this.dispatch('created');
        this.attr('searchName', '');
      }, (err) => {
        handleAjaxError(err);
      }).always(() => {
        this.attr('isDisabled', false);
      });
    },
  }),
});
