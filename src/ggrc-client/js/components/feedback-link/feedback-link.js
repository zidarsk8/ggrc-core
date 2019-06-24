/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './templates/feedback-link.stache';

const viewModel = CanMap.extend({
  define: {
    link: {
      get() {
        return GGRC.config.CREATE_ISSUE_URL;
      },
    },
    title: {
      get() {
        return _.capitalize(GGRC.config.CREATE_ISSUE_BUTTON_NAME) ||
          'Feedback';
      },
    },
  },
});

export default CanComponent.extend({
  tag: 'feedback-link',
  view: can.stache(template),
  leakScope: true,
  viewModel,
});
