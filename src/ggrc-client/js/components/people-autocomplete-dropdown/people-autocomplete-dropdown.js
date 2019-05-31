/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canMap from 'can-map';
import canComponent from 'can-component';
import canStache from 'can-stache';
import '../people-autocomplete/people-autocomplete-wrapper/people-autocomplete-wrapper';
import '../people-autocomplete/people-autocomplete-results/people-autocomplete-results';
import template from './people-autocomplete-dropdown.stache';

/**
 * Wrapper for people-autocomplete-wrapper and people-autocomplete-results
**/

export default canComponent.extend({
  tag: 'people-autocomplete-dropdown',
  view: canStache(template),
  viewModel: canMap.extend({
    showResults: false,
    currentValue: null,
    personSelected({item: person}) {
      this.dispatch({type: 'personSelected', person});
      this.attr('showResults', false);
      this.attr('currentValue', null);
    },
    onActionKey(keyCode) {
      if (this.attr('showResults')) {
        // trigger setter of 'actionKey'
        this.attr('actionKey', keyCode);
        this.attr('actionKey', null);
      }
    },
  }),
  events: {
    '{window} click'() {
      this.viewModel.attr('showResults', false);
    },
  },
});
