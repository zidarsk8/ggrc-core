/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import canStache from 'can-stache';
import CanMap from 'can-map';
import CanComponent from 'can-component';
export default CanComponent.extend({
  tag: 'action-toolbar-control',
  view: canStache(
    '<div class="action-toolbar__controls-item"><content/></div>'
  ),
  leakScope: true,
  viewModel: CanMap.extend({}),
});

