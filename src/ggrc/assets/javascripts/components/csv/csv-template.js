/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

var template = can.view(GGRC.mustache_path +
  '/import_export/create_template.mustache');

can.Component.extend({
  tag: 'csv-template',
  template: template,
  scope: {
    url: '/_service/export_csv',
    selected: [],
    importable: GGRC.Bootstrap.importable
  },
  events: {
    '#importSelect change': function (el, ev) {
      var $items = el.find(':selected');
      var selected = this.scope.attr('selected');

      $items.each(function () {
        var $item = $(this);
        if (_.findWhere(selected, {value: $item.val()})) {
          return;
        }
        return selected.push({
          name: $item.attr('label'),
          value: $item.val()
        });
      });
    },
    '.import-button click': function (el, ev) {
      var data;
      ev.preventDefault();
      data = _.map(this.scope.attr('selected'), function (el) {
        return {
          object_name: el.value,
          fields: 'all'
        };
      });
      if (!data.length) {
        return;
      }

      GGRC.Utils.export_request({
        data: data
      }).then(function (data) {
        GGRC.Utils.download('import_template.csv', data);
      })
        .fail(function (data) {
          $('body').trigger('ajax:flash', {
            error: $(data.responseText.split('\n')[3]).text()
          });
        });
    },
    '.import-list a click': function (el, ev) {
      var index = el.data('index');
      var item = this.scope.attr('selected').splice(index, 1)[0];

      ev.preventDefault();

      this.element.find('#importSelect option:selected').each(function () {
        var $item = $(this);
        if ($item.val() === item.value) {
          $item.prop('selected', false);
        }
      });
    }
  }
});
