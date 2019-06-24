/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
import '../release-notes-list/release-notes-list';

import template from './release-notes-modal.stache';

const viewModel = CanMap.extend({
  define: {
    shortVersion: {
      type: 'string',
      get() {
        if (!GGRC.config.VERSION) {
          return '';
        }

        return GGRC.config.VERSION.replace(/ \(.*\)/, '');
      },
    },
    releaseNotesDate: {
      type: 'string',
      get() {
        return moment(BUILD_DATE).format('MMM D, YYYY');
      },
    },
  },
  modalTitle: 'What\'s new',
});

export default CanComponent.extend({
  tag: 'release-notes-modal',
  view: can.stache(template),
  leakScope: true,
  viewModel,
});
