/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canComponent from 'can-component';
import canStache from 'can-stache';
import canMap from 'can-map';
import template from './create-saved-search.stache';
import SavedSearch from '../../../models/service-models/saved-search';
import {handleAjaxError} from '../../../plugins/utils/errors-utils';
import {notifier} from '../../../plugins/utils/notifiers-utils';
import pubSub from '../../../pub-sub';

export default canComponent.extend({
  tag: 'create-saved-search',
  template: canStache(template),
  leakScope: false,
  viewModel: canMap.extend({
    filterItems: null,
    mappingItems: null,
    statusItem: null,
    parentItems: null,
    parentInstance: null,
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
      let parentInstance = this.attr('parentInstance') &&
        this.attr('parentInstance').serialize();
      if (parentInstance) {
        if (parentItems) {
          parentItems.push(parentInstance);
        } else {
          parentItems = [parentInstance];
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

      if (!this.attr('searchName')) {
        notifier('error', 'Saved search name can\'t be blank');
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
      return savedSearch.save().then((savedSearch) => {
        pubSub.dispatch({
          type: 'savedSearchCreated',
          search: savedSearch,
        });
        this.attr('searchName', '');
      }, (err) => {
        handleAjaxError(err);
      }).always(() => {
        this.attr('isDisabled', false);
      });
    },
  }),
});
