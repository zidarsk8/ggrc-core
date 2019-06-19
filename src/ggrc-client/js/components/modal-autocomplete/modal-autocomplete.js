/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canComponent from 'can-component';
import canMap from 'can-map';
import {
  onAutocompleteSelect,
  onAutocompleteKeyup,
} from './utils';

const viewModel = canMap.extend({
  instance: null,
  isNewInstance: false,
  isQueryAutocompleteEnabled: false,
  initAutocomplete() {
    const $autocompleteInput = this.attr('element').find('[data-lookup]');
    const options = {
      onSelectCallback: onAutocompleteSelect(
        this.attr('instance'),
        this.attr('isNewInstance'),
      ),
    };

    if (this.attr('isQueryAutocompleteEnabled')) {
      $autocompleteInput.ggrc_query_autocomplete(options);
    } else {
      $autocompleteInput.ggrc_autocomplete(options);
    }
  },
});

const events = {
  inserted() {
    const viewModel = this.viewModel;
    viewModel.attr('element', this.element);

    viewModel.initAutocomplete();
  },
  // every time when instance is changed need to re-init autocomplete
  // (for example, it's changed when "Save & Add Another" button is clicked
  // on Create modals)
  '{viewModel} instance'() {
    this.viewModel.initAutocomplete();
  },
  'input[data-lookup] keyup'(el, ev) {
    onAutocompleteKeyup(this.viewModel.attr('instance'), el, ev);
  },
};

export default canComponent.extend({
  tag: 'modal-autocomplete',
  viewModel,
  events,
});
