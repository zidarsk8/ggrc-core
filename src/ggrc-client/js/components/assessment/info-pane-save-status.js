/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  GGRC.Components('infoPaneSaveStatus', {
    tag: 'info-pane-save-status',
    viewModel: {
      infoPaneSaving: false,
    },
  });
})(window.can, window.GGRC);
