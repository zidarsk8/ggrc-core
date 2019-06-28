/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canStache from 'can-stache';
import canMap from 'can-map';
import CanComponent from 'can-component';
import template from './add-object-button.stache';

export default CanComponent.extend({
  tag: 'add-object-button',
  view: canStache(template),
  leakScope: true,
  viewModel: canMap.extend({
    instance: null,
    linkclass: '',
    content: '',
    text: '',
    singular: '',
    plural: '',
  }),
});
