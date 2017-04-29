/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/mapped-objects/directly-mapped-objects.mustache');
  var tag = 'directly-mapped-objects';
  /**
   * Directly mapped objects view component
   */
  can.Component.extend({
    tag: tag,
    template: tpl,
    viewModel: can.Map.extend({
      define: {
        emptyMessage: {
          type: 'string',
          value: ''
        }
      },
      isLoading: false,
      items: null,
      mappedItems: [],
      modelName: '@',
      parentInstance: null,
      init: function () {
        this.getMappedObjects();
      },
      getMappedObjects: function () {
        var items = this.attr('items');
        var modelName = this.attr('modelName');
        var ids = items.map(function (item) { return item.id; });
        var objects = [];

        CMS.Models[modelName].findAll({
          id__in: ids.join(',')
        })
        .then(function (data) {
          objects = data.map(function (item) {
            return item;
          });
          this.attr('mappedItems').replace(objects);
        }.bind(this))
        .always(function () {
          this.attr('isLoading', false);
        }.bind(this))
      }
    }),
    events: {
      '{viewModel} items': function () {
        this.viewModel.getMappedObjects();
      }
    }
  });
})(window.can, window.GGRC);
