/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/advanced-search/advanced-search-mapping-group.mustache');

  var viewModel = can.Map.extend({
    items: can.List(),
    modelName: null,
    root: false,
    availableAttributes: can.List(),
    addMappingCriteria: function () {
      var items = this.attr('items');
      items.push(GGRC.Utils.AdvancedSearch.create.operator('AND'));
      items.push(GGRC.Utils.AdvancedSearch.create.mappingCriteria());
    },
    removeMappingCriteria: function (item) {
      var items = this.attr('items');
      var index = items.indexOf(item);
      // we have to remove operator in front of each item except the first
      if (index > 0) {
        index--;
      }

      // if there is only 1 item in group we have to remove the whole group
      if (items.length === 1) {
        this.remove();
        return;
      }

      items.splice(index, 2);
    },
    remove: function () {
      this.dispatch('remove');
    }
  });

  GGRC.Components('advancedSearchMappingGroup', {
    tag: 'advanced-search-mapping-group',
    template: template,
    viewModel: viewModel
  });
})(window.can, window.GGRC);
