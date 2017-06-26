/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/advanced-search/advanced-search-filter-group.mustache');

  /**
   * Filter Group view model.
   * Contains logic used in Filter Group component
   * @constructor
   */
  var viewModel = can.Map.extend({
    /**
     * Contains Filter Attributes and Operators.
     * @type {can.List}
     */
    items: can.List(),
    /**
     * Contains available attributes for specific model.
     * @type {can.List}
     */
    availableAttributes: can.List(),
    /**
     * Adds Filter Operator and Filter Attribute to the collection.
     */
    addFilterCriterion: function () {
      var items = this.attr('items');
      items.push(GGRC.Utils.AdvancedSearch.create.operator('AND'));
      items.push(GGRC.Utils.AdvancedSearch.create.attribute());
    },
    /**
     * Removes Filter Operator and Filter Attribute from the collection.
     * @param {can.Map} item - Filter Attribute.
     */
    removeFilterCriterion: function (item) {
      var items = this.attr('items');
      var index = items.indexOf(item);
      // we have to remove operator in front of each item except the first
      if (index > 0) {
        index--;
      }

      // if there is only 1 item in group we have to remove a whole group
      if (items.length === 1) {
        this.remove();
        return;
      }

      items.splice(index, 2);
    },
    /**
     * Dispatches event meaning that the component should be removed from parent container.
     */
    remove: function () {
      this.dispatch('remove');
    }
  });

  /**
   * Filter Group is a component allowing to compose Filter Attributes and Operators.
   */
  GGRC.Components('advancedSearchFilterGroup', {
    tag: 'advanced-search-filter-group',
    template: template,
    viewModel: viewModel
  });
})(window.can, window.GGRC);
