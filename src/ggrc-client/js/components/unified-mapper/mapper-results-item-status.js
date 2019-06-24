/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './templates/mapper-results-item-status.stache';

export default CanComponent.extend({
  tag: 'mapper-results-item-status',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    itemData: {},
  }),
});
