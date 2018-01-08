/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/mapper-results-item-status.mustache';

(function (can, GGRC) {
  'use strict';

  GGRC.Components('mapperResultsItemStatus', {
    tag: 'mapper-results-item-status',
    template: template,
    viewModel: {
      itemData: {}
    }
  });
})(window.can, window.GGRC);
