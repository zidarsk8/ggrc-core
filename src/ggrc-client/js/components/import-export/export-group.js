/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './templates/export-group.mustache';

let url = can.route.deparam(window.location.search.substr(1));
let panelModel = can.Map({
  models: null,
  type: 'Program',
  filter: '',
  relevant: can.compute(function () {
    return new can.List();
  }),
  attributes: new can.List(),
  localAttributes: new can.List(),
  mappings: new can.List(),
});

export default can.Component.extend('exportGroup', {
  tag: 'export-group',
  template,
  viewModel: {
    index: 0,
    'export': '@',
  },
  events: {
    inserted: function () {
      this.addPanel({
        type: url.model_type || 'Program',
        isSnapshots: url.isSnapshots,
      });
    },
    addPanel: function (data) {
      let index = this.viewModel.attr('index') + 1;

      data = data || {};
      if (!data.type) {
        data.type = 'Program';
      } else if (data.isSnapshots === 'true') {
        data.snapshot_type = data.type;
        data.type = 'Snapshot';
      }

      this.viewModel.attr('index', index);
      return this.viewModel.attr('panels.items')
        .push(new panelModel(data));
    },
    getIndex: function (el) {
      return Number($(el.closest('export-panel'))
        .viewModel().attr('panel_number'));
    },
    '.remove_filter_group click': function (el, ev) {
      let index = this.getIndex(el);

      ev.preventDefault();
      this.viewModel.attr('panels.items').splice(index, 1);
    },
    '{viewModel.export} addPanel': function () {
      this.addPanel();
    },
  },
});
