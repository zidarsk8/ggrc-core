/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC) {
  'use strict';

  can.Component.extend('mapperResultsItemAttrs', {
    tag: 'mapper-results-item-attrs',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-results-item-attrs.mustache'
    ),
    viewModel: {
      instance: null,
      selectedColumns: []
    }
  });
})(window.can, window.GGRC);
