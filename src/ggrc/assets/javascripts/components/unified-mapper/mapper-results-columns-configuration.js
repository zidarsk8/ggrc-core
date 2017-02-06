/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC, CMS) {
  'use strict';

  can.Component.extend('mapperResultsColumnsConfiguration', {
    tag: 'mapper-results-columns-configuration',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-results-columns-configuration.mustache'
    ),
    viewModel: {
      modelType: '',
      selectedColumns: [],
      availableColumns: [],
      columns: {},
      displayPrefs: null,
      init: function () {
        var self = this;
        this.initializeColumns();
        CMS.Models.DisplayPrefs.getSingleton().then(function (displayPrefs) {
          self.attr('displayPrefs', displayPrefs);
        });
      },
      getModel: function () {
        return CMS.Models[this.attr('modelType')];
      },
      initializeColumns: function () {
        var selectedColumns = can.makeArray(this.attr('selectedColumns'));
        var availableColumns = can.makeArray(this.attr('availableColumns'));
        var self = this;
        this.attr('columns', {});
        availableColumns
          .forEach(function (attr) {
            if (selectedColumns.some(function (selectedAttr) {
              return selectedAttr.attr_name === attr.attr_name;
            })) {
              self.attr('columns.' + attr.attr_name, true);
            } else {
              self.attr('columns.' + attr.attr_name, false);
            }
          });
      },
      setColumns: function () {
        var availableColumns = can.makeArray(this.attr('availableColumns'));
        var displayPrefs = this.attr('displayPrefs');
        var selected = [];
        var selectedNames = [];
        var current;
        can.each(this.attr('columns'), function (v, k) {
          current = availableColumns.find(function (attr) {
            return attr.attr_name === k;
          });
          current.display_status = v;
          if (v) {
            selected.push(current);
            if (!current.mandatory) {
              selectedNames.push(k);
            }
          }
        });
        displayPrefs.setTreeViewHeaders(
          this.getModel().model_singular,
          selectedNames
        );
        displayPrefs.save();
        this.attr('selectedColumns', selected);
      },
      stopPropagation: function (context, el, ev) {
        ev.stopPropagation();
      }
    },
    events: {
      '{viewModel} availableColumns': function () {
        this.viewModel.initializeColumns();
      },
      '{viewModel} selectedColumns': function () {
        this.viewModel.initializeColumns();
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
