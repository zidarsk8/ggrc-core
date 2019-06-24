/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './templates/change-request-link.stache';

const viewModel = CanMap.extend({
  define: {
    link: {
      get() {
        return GGRC.config.CHANGE_REQUEST_URL;
      },
    },
  },
});

export default CanComponent.extend({
  tag: 'change-request-link',
  view: can.stache(template),
  leakScope: true,
  viewModel,
});
