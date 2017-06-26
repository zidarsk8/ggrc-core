/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/advanced-search/advanced-search-mapping-container.mustache');

  /**
   * Mapping Container view model.
   * Contains logic used in Mapping Container component
   * @constructor
   */
  var viewModel = can.Map.extend({
    /**
     * Contains Mapping Criteria, Groups and Operators.
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
     * Contains available attributes for specific model.
     * @type {can.List}
     */
    availableAttributes: can.List(),
    /**
     * Adds Mapping Criteria and Operator to the collection.
     * Adds only Mapping Criteria if collection is empty.
     */
    addMappingCriteria: function () {
      var items = this.attr('items');
      if (items.length) {
        items.push(GGRC.Utils.AdvancedSearch.create.operator('AND'));
      }
      items.push(GGRC.Utils.AdvancedSearch.create.mappingCriteria());
    },
    /**
     * Removes Filter Operator and Advanced Search mapping item from the collection.
     * @param {can.Map} item - Advanced Search mapping item.
     */
    removeMappingCriteria: function (item) {
      var items = this.attr('items');
      var index = items.indexOf(item);
      // we have to remove operator in front of each item except the first
      if (index > 0) {
        index--;
      }
      items.splice(index, 2);
    },
    /**
     * Transforms Mapping Criteria to Mapping Group.
     * @param {can.Map} criteria - Mapping Criteria.
     */
    createGroup: function (criteria) {
      var items = this.attr('items');
      var index = items.indexOf(criteria);
      items.attr(index, GGRC.Utils.AdvancedSearch.create.group([
        criteria,
        GGRC.Utils.AdvancedSearch.create.operator('AND'),
        GGRC.Utils.AdvancedSearch.create.mappingCriteria()
      ]));
    }
  });

  /**
   * Mapping Container is a component allowing to compose Mapping Criteria, Groups and Operators.
   */
  GGRC.Components('advancedSearchMappingContainer', {
    tag: 'advanced-search-mapping-container',
    template: template,
    viewModel: viewModel
  });
})(window.can, window.GGRC);
