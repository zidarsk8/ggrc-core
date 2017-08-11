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
  var viewModel = GGRC.VM.AdvancedSearchContainer.extend({
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
     * Adds Filter Operator and Mapping Criteria to the collection.
     */
    addMappingCriteria: function () {
      var items = this.attr('items');
      items.push(GGRC.Utils.AdvancedSearch.create.operator('AND'));
      items.push(GGRC.Utils.AdvancedSearch.create.mappingCriteria());
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
