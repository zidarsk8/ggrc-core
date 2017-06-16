/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/advanced-search/advanced-search-mapping-container.mustache');

  var viewModel = can.Map.extend({
    items: can.List(),
    modelName: null,
    availableAttributes: can.List(),
    addMappingCriteria: function () {
      var items = this.attr('items');
      if (items.length) {
        items.push(GGRC.Utils.AdvancedSearch.create.operator('AND'));
      }
      items.push(GGRC.Utils.AdvancedSearch.create.mappingCriteria());
    },
    removeFilterCriterion: function (item) {
      var items = this.attr('items');
      var index = items.indexOf(item);
      if (items.length === index + 1) {
        index--;
      }
      items.splice(index, 2);
    },
    createGroup: function (attribute) {
      var items = this.attr('items');
      var index = items.indexOf(attribute);
      items.attr(index, GGRC.Utils.AdvancedSearch.create.group([attribute]));
    }
  });

  GGRC.Components('advancedSearchMappingContainer', {
    tag: 'advanced-search-mapping-container',
    template: template,
    viewModel: viewModel
  });
})(window.can, window.GGRC);
