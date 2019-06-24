/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import '../../person/person-data';
import template from './person-form-field-view.stache';

export default CanComponent.extend({
  tag: 'person-form-field-view',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    value: null,
    disabled: false,
  }),
});
