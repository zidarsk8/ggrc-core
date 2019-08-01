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
  view: canStache(template),
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

      /*
      "parentInstance" - current parent instance (when sitting on some object page).
        For example: "Audit" instance is always parent instance for Assessments, when
        sitting on Audit page, Assessments tab.
      "parentItems" - parent instances from previous contexts.
        For example:
          1. Open any Regulation page (for example: "Regulation #1").
          2. Open "Programs" tab.
          3. Open advanced saved search.
          4. Filter contains text: "MAPPED TO REGULATION: Regulation #1".
            It happens because "Regulation #1" is parent instance for programs.
          5. Save current search (for example: "Saved search #1").
          6. Open any Objective page (for example: "Objective #1").
          7. Open "Programs" tab.
          8. Open advanced saved search.
          9. Filter contains text: "MAPPED TO OBJECTIVE: Objective #1".
            It happens because "Objective #1" is parent instance for programs right
            now.
          10. Select previously saved search from point 5 ("Saved search #1").
          11. Filter contains text:
            - "MAPPED TO OBJECTIVE: Objective #1"
            - "MAPPED TO REGULATION: Regulation #1".

        In this case "Objective #1" is current Parent Instance and "Regulation #1" is
        previous Parent Instance that was saved in step 5 and now is item in Parent
        Items.

        "parentItems" array can contain 0 - n items.
        Depends on previously saved search
      */
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
