/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC) {
  'use strict';

  can.Component.extend('mapperToolbar', {
    tag: 'mapper-toolbar',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-toolbar.mustache'
    ),
    viewModel: {
      filter: '',
      mapper: {},
      onSubmit: function () {
        this.dispatch('submit');
      },
      reset: function () {
        $('mapper-filter').viewModel().reset();
      }
    }
  });
})(window.can, window.GGRC);
