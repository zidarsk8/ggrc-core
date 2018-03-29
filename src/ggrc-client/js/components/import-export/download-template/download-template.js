/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import '../../dropdown/multiselect-dropdown';
import template from './download-template.mustache';
import {exportRequest, download} from '../import-export-utils';

const tag = 'download-template';
const CSV_FILE_NAME = 'import_template.csv';
const importOptions = GGRC.Bootstrap.importable.map((el) => {
  return {
    name: el.model_singular,
    value: el.title_plural,
  };
});
const viewModel = can.Map.extend({
  define: {},
  modalTitle: 'Download Template',
  modalState: {
    open: false,
    result: {},
  },
  selected: [],
  importableModels: importOptions,
  close() {
    this.attr('modalState.open', false);
    this.attr('selected').replace([]);
    this.attr('importableModels').forEach((element) => {
      element.attr('checked', false);
    });
  },
  showDialog() {
    this.attr('modalState.open', true);
  },
  selectItems(event) {
    let selected = event.selected;

    if (!selected || !selected.length) {
      this.attr('selected', []);
    } else {
      this.attr('selected', selected);
    }
  },
  downloadCSV() {
    let selected = this.attr('selected');
    let objects = [];

    if (!selected.length) {
      return;
    }

    objects = Array.from(selected).map(({name}) => {
      return {
        object_name: name,
        fields: 'all',
      };
    });

    return exportRequest({
      data: {
        objects,
        export_to: 'csv',
      },
    }).then(function (data) {
      download(CSV_FILE_NAME, data);
    }).always(() => {
      this.close();
    });
  },
});

export default can.Component.extend({
  tag,
  template,
  viewModel,
});
