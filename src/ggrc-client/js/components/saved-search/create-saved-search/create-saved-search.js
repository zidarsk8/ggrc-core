/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import SavedSearch from '../../../models/service-models/saved-search';
import { notifierXHR } from '../../../plugins/utils/notifiers-utils';
import { handleAjaxError } from '../../../plugins/utils/errors-utils';

export default can.Component.extend({
  tag: 'create-saved-search',
  template: can.stache(`
    <input {($value)}="{searchName}" type="text" placeholder="Type to Save Search">
    <button ($click)="saveSearch()" type="button" class="btn btn-small btn-green">Save Search</button>
  `),
  leakScope: false,
  viewModel: can.Map.extend({
    query: null,
    filterItems: null,
    mappingItems: null,
    statusItem: null,
    searchName: '',
    objectType: '',
    saveSearch() {
      const filters = {
        filterItems: this.attr('filterItems').serialize(),
        mappingItems: this.attr('mappingItems').serialize(),
        statusItem: this.attr('statusItem').serialize(),
      };

      const savedSearch = new SavedSearch({
        name: this.attr('searchName'),
        object_type: this.attr('objectType'),
        filters,
      })
      return savedSearch.save().then(() => {
        this.dispatch('created');
      }, (err) => {
        handleAjaxError(err);
      });
    },
  }),
});
