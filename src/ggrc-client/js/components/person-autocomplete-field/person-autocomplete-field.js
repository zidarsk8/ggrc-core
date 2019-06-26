/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canComponent from 'can-component';
import canStache from 'can-stache';
import template from './person-autocomplete-field.stache';
import actionKeyable from '../view-models/action-keyable';

const KEYS_TO_LISTEN = ['ArrowUp', 'ArrowDown', 'Enter'];

/**
 * Another person autocomplete field
 **/

export default canComponent.extend({
  tag: 'person-autocomplete-field',
  view: canStache(template),
  viewModel: actionKeyable.extend({
    personEmail: '',
    showResults: false,
    inputId: '',
    tabindex: -1,
    placeholder: '',
    personSelected({person}) {
      this.attr('personEmail', person.email);
    },
    onKeyDown(event) {
      if (KEYS_TO_LISTEN.includes(event.code)) {
        this.onActionKey(event.keyCode);
        event.preventDefault();
      }
    },
    onKeyUp(event) {
      const inputValue = event.target.value;
      this.attr('personEmail', inputValue);
      if (!KEYS_TO_LISTEN.includes(event.code)) {
        this.attr('searchValue', inputValue);
      }
    },
  }),
  events: {
    '{window} click'() {
      this.viewModel.attr('showResults', false);
    },
  },
});
