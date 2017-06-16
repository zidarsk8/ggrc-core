/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can, _) {
  'use strict';

  GGRC.Utils.AdvancedSearch = (function () {
    var create = {
      attribute: function (value) {
        return {
          type: 'attribute',
          value: value || { }
        };
      },
      group: function (value) {
        return {
          type: 'group',
          value: value || []
        };
      },
      operator: function (value) {
        return {
          type: 'operator',
          value: value || ''
        };
      },
      state: function (value) {
        return {
          type: 'state',
          value: value || { }
        };
      },
      mappingCriteria: function (value) {
        return {
          type: 'mappingCriteria',
          value: value || { }
        };
      }
    };

    var richOperators = {
      ANY: function (values) {
        return _.map(values, function (value) {
          return '"Status"="' + value + '"';
        }).join(' OR ');
      },
      NONE: function (values) {
        return _.map(values, function (value) {
          return '"Status"!="' + value + '"';
        }).join(' AND ');
      }
    };
    var builders = {
      attribute: attributeToFilter,
      operator: operatorToFilter,
      state: stateToFilter,
      group: groupToFilter,
      mappingCriteria: mappingCriteriaToFilter
    };

    function attributeToFilter(attribute) {
      return '"' + attribute.field +
             '" ' + attribute.operator +
             ' "' + attribute.value + '"';
    }
    function operatorToFilter(operator) {
      return ' ' + operator + ' ';
    }
    function stateToFilter(state) {
      return '(' + GGRC.Utils.State.buildStatusFilter(
        state.items,
        richOperators[state.operator],
        state.modelName) + ')';
    }
    function groupToFilter(items) {
      return '(' + buildFilterString(items) + ')';
    }
    function buildFilterString(items) {
      var result = '';
      _.each(items, function (item) {
        result += builders[item.type](item.value);
      });
      return result;
    }

    function mappingCriteriaToFilter(criteria, request) {
      var criteriaId = addMappingCriteria(criteria, request);
      return previousToFilter(criteriaId);
    }
    function previousToFilter(criteriaId) {
      return '#__previous__,' + criteriaId + '#';
    }
    function addMappingCriteria(mapping, request) {
      var filterObject = GGRC.query_parser
        .parse(attributeToFilter(mapping.filter.value));
      var criteriaId;
      if (mapping.mappedTo) {
        criteriaId = addMappingCriteria(mapping.mappedTo.value, request);
        filterObject = GGRC.query_parser.join_queries(
          filterObject,
          GGRC.query_parser.parse(previousToFilter(criteriaId))
        );
      }
      request.push({
        object_name: mapping.objectName,
        type: 'ids',
        filters: filterObject
      });
      return request.length - 1;
    }
    function parseMappings(data, request) {
      var result = '';
      _.each(data, function (item) {
        result += builders[item.type](item.value, request);
      });
      return GGRC.query_parser.parse(result);
    }

    return {
      buildFilterString: buildFilterString,
      create: create,
      parseMappings: parseMappings
    };
  })();
})(window.GGRC, window.can, window._);
