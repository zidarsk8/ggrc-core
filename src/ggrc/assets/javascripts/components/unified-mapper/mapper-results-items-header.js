/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC, CMS) {
  'use strict';

  can.Component.extend('mapperResultsItemsHeader', {
    tag: 'mapper-results-items-header',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-results-items-header.mustache'
    ),
    viewModel: {
      availableColumns: [],
      selectedColumns: [],
      modelType: '',
      refreshCbs: null,
      displayPrefs: null,
      init: function () {
        var self = this;
        this.attr('refreshCbs').add(this.setColumnsConfiguration.bind(this));
        CMS.Models.DisplayPrefs.getSingleton().then(function (displayPrefs) {
          self.attr('displayPrefs', displayPrefs);
        });
      },
      destroy: function () {
        this.attr('refreshCbs').remove(this.setColumnsConfiguration.bind(this));
      },
      setColumnsConfiguration: function () {
        var columns =
          GGRC.Utils.TreeView.getColumnsForModel(
            this.attr('modelType'),
            this.attr('displayPrefs')
          );
        this.attr('availableColumns', columns.availableColumns);
        this.attr('selectedColumns', columns.selectedColumns);
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
