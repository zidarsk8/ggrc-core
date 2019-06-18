/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as StateUtils from './state-utils';
import QueryParser from '../../generated/ggrc_filter_query_parser';
import {makeRelevantFilter} from './query-api-utils';

/**
 * Factory allowing to create Advanced Search Filter Items.
 */
export const create = {
  /**
   * Creates Filter Attribute.
   * @param {object} value - Filter Attribute data.
   * @return {object} - Attribute model.
   */
  attribute: (value) => {
    return {
      type: 'attribute',
      value: value || { },
    };
  },
  /**
   * Creates Group.
   * @param {Array} value - Group data.
   * @return {object} - Group model.
   */
  group: (value) => {
    return {
      type: 'group',
      value: value || [],
    };
  },
  /**
   * Creates Operator.
   * @param {string} value - Operator name.
   * @return {object} - Operator model.
   */
  operator: (value) => {
    return {
      type: 'operator',
      value: value || '',
    };
  },
  /**
   * Creates Filter State
   * @param {object} value - State data.
   * @return {object} - State model.
   */
  state: (value) => {
    return {
      type: 'state',
      value: value || { },
    };
  },
  /**
   * Creates Mapping Criteria
   * @param {object} value - Mapping Criteria data.
   * @return {object} - Mapping Criteria model.
   */
  mappingCriteria: (value) => {
    return {
      type: 'mappingCriteria',
      value: value || { },
    };
  },
  parent: (value) => {
    return {
      type: 'parent',
      value: value || { },
    };
  },
};

/**
 * Adds Mapping Criteria as separate QueryAPI request.
 * @param {object} mapping - Mapping Criteria model value.
 * @param {Array} request - Collection of QueryAPI sub-requests.
 * @return {number} - QueryAPI request id.
 */
export const addMappingCriteria = (mapping, request) => {
  let filterObject = builders.attribute(mapping.filter.value);

  if (mapping.mappedTo) {
    let relevantResult =
      builders[mapping.mappedTo.type](mapping.mappedTo.value, request);
    filterObject = QueryParser.joinQueries(filterObject, relevantResult);
  }

  request.push({
    object_name: mapping.objectName,
    type: 'ids',
    filters: filterObject,
  });

  return request.length - 1;
};

/**
 * Convertes collection of Advanced Search models to reverse polish notation.
 * @param {Array} items - Collection of Advanced Search models.
 * @return {Array} - Collection of Advanced Search models sorted in reverse polish notation.
 */
export const reversePolishNotation = (items) => {
  const result = [];
  const stack = [];
  const priorities = {
    OR: 1,
    AND: 2,
  };

  items.forEach((item) => {
    if (item.type !== 'operator') {
      result.push(item);
    } else {
      if (!_.isEmpty(stack) &&
        priorities[item.value] <= priorities[_.last(stack).value]) {
        result.push(stack.pop());
      }
      stack.push(item);
    }
  });

  while (stack.length) {
    result.push(stack.pop());
  }

  return result;
};

/**
 * Contains QueryAPI filter expression builders.
 */
export const builders = {
  /**
   * Transforms Filter Attribute model to valid QueryAPI filter expression.
   * @param {object} attribute - Filter Attribute model value.
   * @return {object} - Valid QueryAPI filter expression.
   */
  attribute: (attribute) => {
    return {
      expression: {
        left: attribute.field,
        op: {name: attribute.operator},
        right: attribute.value.trim(),
      },
    };
  },
  /**
   * Transforms State model to valid QueryAPI filter expression.
   * @param {object} state - State model value.
   * @return {object} - Valid QueryAPI filter expression.
   */
  state: (state) => {
    let inverse = state.operator === 'NONE';
    return StateUtils.buildStatusFilter(state.items, state.modelName, inverse);
  },
  /**
   * Transforms Group model to valid QueryAPI filter expression.
   * @param {array} items - Group model value.
   * @param {Array} request - Collection of QueryAPI sub-requests.
   * @return {object} - Valid QueryAPI filter expression.
   */
  group: (items, request) => {
    items = reversePolishNotation(items);

    const stack = [];
    items.forEach((item) => {
      if (item.type !== 'operator') {
        stack.push(builders[item.type](item.value, request));
      } else {
        let joinedValue = QueryParser.
          joinQueries(stack.pop(), stack.pop(), item.value);
        stack.push(joinedValue);
      }
    });

    return stack.pop() || {expression: {}};
  },
  /**
   * Transforms Mapping Criteria model to valid QueryAPI filter expression.
   * @param {object} criteria - Mapping Criteria model value.
   * @param {Array} request - Collection of QueryAPI sub-requests.
   * @return {object} - Valid QueryAPI filter expression.
   */
  mappingCriteria: (criteria, request) => {
    let criteriaId = addMappingCriteria(criteria, request);
    return {
      expression: {
        object_name: '__previous__',
        op: {name: 'relevant'},
        ids: [criteriaId],
      },
    };
  },
  parent: (parent) => {
    return makeRelevantFilter(parent);
  },
};

/**
 * Builds QueryAPI valid filter expression based on Advanced Search models.
 * @param {Array} data - Collection of Advanced Search models.
 * @param {Array} request - Collection of QueryAPI sub-requests.
 * @return {object} - valid QueryAPI filter expression.
 */
export const buildFilter = (data, request) => {
  let result = builders.group(data, request);
  return result;
};

/**
 * Fills statusItem with default values for passed modelName.
 * @param {canMap} state - Current state.
 * @param {String} modelName - Name of the model to find states of.
 * @return {canMap} - updated state.
 */
export const setDefaultStatusConfig = (state, modelName) => {
  const items = StateUtils.getStatesForModel(modelName);
  state.attr('items', items);
  state.attr('operator', 'ANY');
  state.attr('modelName', modelName);
  return state;
};

/**
 * Convert JSON filter to Object
 * @param {string} json - JSON string
 * @return {Object} - parsed advanced search filter
 */
export const parseFilterJson = (json) => {
  let {
    filterItems,
    mappingItems,
    statusItem,
    parentItems,
  } = JSON.parse(json);

  return {
    filterItems,
    mappingItems,
    statusItem,
    parentItems,
  };
};

/**
 * Filter parent items to remove duplicates
 * @param {Object} parent - parent attribute of Advanced search
 * @param {Array} parentItems - parentItems attribute of Advanced search
 * @return {Array} - filtered parentItems
 */
export const filterParentItems = (parent, parentItems) => {
  return parentItems = parentItems.filter((item) =>
    item.value.id !== parent.value.id ||
    item.value.type !== parent.value.type);
};

/**
 * Apply saved search filter to current advanced search
 * @param {can.Map} advancedSearch - current advanced search
 * @param {Object} savedSearch - saved search
 */
export const applySavedSearchFilter = (advancedSearch, savedSearch) => {
  const savedSearchFilter = parseFilterJson(savedSearch.filters);

  const parent = advancedSearch.attr('parent');
  if (parent && savedSearchFilter.parentItems) {
    savedSearchFilter.parentItems =
      filterParentItems(parent, savedSearchFilter.parentItems);
  }

  advancedSearch.attr('filterItems', savedSearchFilter.filterItems);
  advancedSearch.attr('mappingItems', savedSearchFilter.mappingItems);
  advancedSearch.attr('parentItems', savedSearchFilter.parentItems);

  const appliedSavedSearch = {
    filterItems: savedSearchFilter.filterItems,
    mappingItems: savedSearchFilter.mappingItems,
    parentItems: savedSearchFilter.parentItems,
    id: savedSearch.id,
  };

  // save applied saved search
  advancedSearch.attr('appliedSavedSearch', appliedSavedSearch);
};

/**
 * Compare applied saved search with current advanced search filter
 * @param {Object} appliedSavedSearch - applied saved search
 * @param {Object} searchFilter - cuurent search filter
 * @return {Boolean} - is current advanced search filter equals to
 * applied save search
 */
export const isSavedSearch = (appliedSavedSearch, searchFilter) => {
  if (!appliedSavedSearch) {
    return false;
  }

  function getParents(parentItems) {
    return parentItems.map((item) => {
      return {
        id: item.value.id,
        type: item.value.type,
      };
    });
  }

  const savedSearchParents = getParents(appliedSavedSearch.parentItems);
  const currentSearchParents = getParents(searchFilter.parentItems);

  return _.isEqual(appliedSavedSearch.filterItems, searchFilter.filterItems) &&
    _.isEqual(appliedSavedSearch.mappingItems, searchFilter.mappingItems) &&
    _.isEqual(savedSearchParents, currentSearchParents);
};

/**
 * Build permalink for saved search
 * @param {Number} searchId - saved search ID
 * @param {String} modelName - model name
 * @return {String} - permalink
 */
export const buildSearchPermalink = (searchId, modelName) => {
  const origin = window.location.origin;
  const pathName = window.location.pathname;
  const url = `${origin}${pathName}`;
  const hash = `#!${modelName}&saved_search=${searchId}`;
  const permalink = `${url}${hash}`;

  return permalink;
};
