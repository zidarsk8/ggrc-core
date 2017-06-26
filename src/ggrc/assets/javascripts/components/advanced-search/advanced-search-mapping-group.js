/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/advanced-search/advanced-search-mapping-group.mustache');

  /**
   * Mapping Group view model.
   * Contains logic used in Mapping Group component.
   * @constructor
   */
  var viewModel = can.Map.extend({
    /**
     * Contains Mapping Criteria and Operators.
     * @type {can.List}
     */
    items: can.List(),
    /**
     * Contains specific model name.
     * @type {string}
     * @example
     * Section
     * Regulation
     */
    modelName: null,
    /**
     * Indicates that Group is created on the root level.
     * @type {boolean}
     */
    root: false,
    /**
     * Contains available attributes for specific model.
     * @type {can.List}
     */
    availableAttributes: can.List(),
    /**
     * Adds Filter Operator and Mapping Criteria to the collection.
     */
    addMappingCriteria: function () {
      var items = this.attr('items');
      items.push(GGRC.Utils.AdvancedSearch.create.operator('AND'));
      items.push(GGRC.Utils.AdvancedSearch.create.mappingCriteria());
    },
    /**
     * Removes Filter Operator and Mapping Criteira from the collection.
     * @param {can.Map} item - Mapping Criteria.
     */
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
    /**
     * Dispatches event meaning that the component should be removed from parent container.
     */
    remove: function () {
      this.dispatch('remove');
    }
  });

  /**
   * Mapping Group is a component allowing to compose Mapping Criteria and Operators.
   */
  GGRC.Components('advancedSearchMappingGroup', {
    tag: 'advanced-search-mapping-group',
    template: template,
    viewModel: viewModel
  });
})(window.can, window.GGRC);
