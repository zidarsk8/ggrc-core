/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './templates/csv-template.mustache';

export default GGRC.Components('csvTemplate', {
  tag: 'csv-template',
  template: template,
  scope: {
    url: '/_service/export_csv',
    selected: [],
    importable: GGRC.Bootstrap.importable,
  },
  events: {
    '#importSelect change': function (el, ev) {
      let $items = el.find(':selected');
      let selected = this.scope.attr('selected');

      $items.each(function () {
        let $item = $(this);
        if (_.findWhere(selected, {value: $item.val()})) {
          return;
        }
        return selected.push({
          name: $item.attr('label'),
          value: $item.val(),
        });
      });
    },
    '.import-button click': function (el, ev) {
      let objects;
      ev.preventDefault();

      objects = _.map(this.scope.attr('selected'), function (el) {
        return {
          object_name: el.value,
          fields: 'all',
        };
      });
      if (!objects.length) {
        return;
      }

      GGRC.Utils.export_request({
        data: {
          objects: objects,
          export_to: 'csv',
        },
      }).then(function (data) {
        GGRC.Utils.download('import_template.csv', data);
      });
    },
    '.import-list a click': function (el, ev) {
      let index = el.data('index');
      let item = this.scope.attr('selected').splice(index, 1)[0];

      ev.preventDefault();

      this.element.find('#importSelect option:selected').each(function () {
        let $item = $(this);
        if ($item.val() === item.value) {
          $item.prop('selected', false);
        }
      });
    },
  },
});
