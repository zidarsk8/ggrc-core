/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/advanced-search/advanced-search-mapping-criteria.mustache');

  var viewModel = can.Map.extend({
    define: {
      criteria: {
        type: '*',
        Value: can.Map,
        set: function (criteria) {
          if (!criteria.filter) {
            criteria.attr('filter',
              GGRC.Utils.AdvancedSearch.create.attribute());
          }
          return criteria;
        }
      },
      canBeGrouped: {
        type: 'boolean',
        value: false,
        get: function () {
          return this.attr('extendable') &&
           !(this.attr('criteria.mappedTo') && !this.attr('childCanBeGrouped'));
        }
      },
      canAddMapping: {
        type: 'boolean',
        value: false,
        get: function () {
          return !this.attr('criteria.mappedTo');
        }
      },
      showPopover: {
        type: 'boolean',
        value: false,
        get: function () {
          return this.attr('canBeGrouped') && this.attr('canAddMapping');
        }
      }
    },
    childCanBeGrouped: false,
    modelName: null,
    root: false,
    extendable: false,
    availableAttributes: can.List(),
    mappingTypes: function () {
      var mappings = GGRC.Mappings
        .get_canonical_mappings_for(this.attr('modelName'));
      var types = _.chain(mappings)
        .keys()
        .map(function (mapping) {
          return CMS.Models[mapping];
        })
        .compact()
        .sortBy('model_singular')
        .filter(function (mapping) {
          return mapping.model_singular && mapping.title_singular;
        })
        .value();

      if (!this.attr('criteria.objectName')) {
        this.attr('criteria.objectName', _.first(types).model_singular);
      }

      return types;
    },
    title: function () {
      if (this.attr('root')) {
        return 'Mapped To';
      }
      return 'Where ' +
              CMS.Models[this.attr('modelName')].title_singular +
              ' is mapped to';
    },
    remove: function () {
      this.dispatch('remove');
    },
    createGroup: function () {
      this.dispatch('createGroup');
    },
    addRelevant: function () {
      this.attr('criteria.mappedTo',
        GGRC.Utils.AdvancedSearch.create.mappingCriteria());
    },
    removeRelevant: function () {
      this.removeAttr('criteria.mappedTo');
    },
    relevantToGroup: function () {
      this.attr('criteria.mappedTo',
        GGRC.Utils.AdvancedSearch.create.group([
          this.attr('criteria.mappedTo'),
          GGRC.Utils.AdvancedSearch.create.operator('AND'),
          GGRC.Utils.AdvancedSearch.create.mappingCriteria()
        ]));
    }
  });

  GGRC.Components('advancedSearchMappingCriteria', {
    tag: 'advanced-search-mapping-criteria',
    template: template,
    viewModel: viewModel,
    leakScope: false
  });
})(window.can, window.GGRC, window.CMS);
