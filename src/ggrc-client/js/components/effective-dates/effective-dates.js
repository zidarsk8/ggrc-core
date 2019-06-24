/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanComponent from 'can-component';
import '../datepicker/datepicker-component';
import template from './effective-dates.stache';

export default CanComponent.extend({
  tag: 'effective-dates',
  view: can.stache(template),
  leakScope: true,
  viewModel: can.Map.extend({
    instance: null,
    configStartDate: {
      label: 'Effective Date',
      helpText: 'Enter the date this object becomes effective.',
      required: false,
    },
  }),
});
