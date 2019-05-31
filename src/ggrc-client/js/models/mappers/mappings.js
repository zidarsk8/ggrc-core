/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getModelByType} from '../../plugins/utils/models-utils';
import * as businessModels from '../business-models';
import Permission from '../../permission';
import config from './mappings-ggrc';

/*
  class Mappings
  represents everything known about how GGRC objects connect to each other.

  a Mappings instance contains the set of known mappings.
  The set of all Mappings instances is used throughout the
  system to build widgets, map and unmap objects, etc.
*/


function getTypeGroups() {
  return {
    entities: {
      name: 'People/Groups',
      items: [],
    },
    scope: {
      name: 'Scope',
      items: [],
    },
    governance: {
      name: 'Governance',
      items: [],
    },
  };
}

/**
 * Return list of allowed for mapping models.
 * Performs checks for
 * @param {String} type - base model type
 * @param {Array} include - array of included models
 * @param {Array} exclude - array of excluded models
 * @return {Array} - list of allowed for mapping Models
 */
function getMappingList(type) {
  if (!type) {
    return [];
  }

  let allowedToMap = getAllowedToMapModels(type);
  let externalMap = getExternalMapModels(type);

  return _.keys(Object.assign({}, allowedToMap, externalMap));
}

/**
 * Checks user permissions for mappings
 * @param {Object} source - the source object the mapping
 * @param {Object} target - the target object of the mapping
 *
 * @return {Boolean} whether user has permissions for mappings
 */
function userHasPermissions(source, target) {
  let hasPermissions = Permission.is_allowed_for('update', source)
    || source.isNew();

  if (target instanceof can.Map) {
    hasPermissions = hasPermissions
      && Permission.is_allowed_for('update', target);
  }

  return hasPermissions;
}

/**
 * Determine if `target` is allowed to be created and mapped to `source`.
 *
 * @param {Object} source - the source object the mapping
 * @param {Object} target - the target object of the mapping
 *
 * @return {Boolean} - true if mapping is allowed, false otherwise
 */
function allowedToCreate(source, target) {
  let targetType = _getType(target);
  let sourceType = _getType(source);

  let allowedTypes = _.keys(getAllowedToCreateModels(sourceType));
  let canCreate = _.includes(allowedTypes, targetType);

  return canCreate && userHasPermissions(source, target);
}

/**
 * Determine if `target` is allowed to be mapped to `source`.
 *
 * @param {Object} source - the source object the mapping
 * @param {Object} target - the target object of the mapping
 *
 * @return {Boolean} - true if mapping is allowed, false otherwise
 */
function allowedToMap(source, target) {
  let targetType = _getType(target);
  let sourceType = _getType(source);

  let mappableTypes = _.keys(getAllowedToMapModels(sourceType));
  let externalTypes = _.keys(getExternalMapModels(sourceType));

  let canMap = _.includes(mappableTypes, targetType) ||
    _.includes(externalTypes, targetType);

  return canMap && userHasPermissions(source, target);
}

/**
 * Determine if `target` is allowed to be mapped to `source` or created and
 * mapped to 'source'.
 *
 * @param {Object} source - the source object the mapping
 * @param {Object} target - the target object of the mapping
 *
 * @return {Boolean} - true if mapping is allowed, false otherwise
 */
function allowedToCreateOrMap(source, target) {
  let sourceType = _getType(source);
  let targetType = _getType(target);

  let mappableTypes = _.keys(getAllowedToMapModels(sourceType));
  let externalTypes = _.keys(getExternalMapModels(sourceType));
  let createTypes = _.keys(getAllowedToCreateModels(sourceType));

  let canCreateOrMap = _.includes(mappableTypes, targetType) ||
    _.includes(createTypes, targetType) ||
    _.includes(externalTypes, targetType);

  return canCreateOrMap && userHasPermissions(source, target);
}

/**
 * Determine if `target` is allowed to be unmapped from `source`.
 *
 * @param {Object} source - the source object the mapping
 * @param {Object} target - the target object of the mapping
 *
 * @return {Boolean} - true if unmapping is allowed, false otherwise
 */
function allowedToUnmap(source, target) {
  let sourceType = _getType(source);
  let targetType = _getType(target);

  let unmappableTypes = _.keys(getAllowedToUnmapModels(sourceType));
  let canUnmap = _.includes(unmappableTypes, targetType);

  return canUnmap && userHasPermissions(source, target);
}

function _getType(object) {
  let type;

  if (object instanceof can.Model) {
    type = object.constructor.model_singular;
  } else {
    type = object.type || object;
  }

  if (type === 'Snapshot') {
    type = object.child_type; // check Snapshot original object type
  }

  return type;
}

/**
 * Returns the list of allowed direct mapping models
 * with possible related mapping models
 * @param {String} type - base model type
 * @return {Array} - list of available mappings
 */
function getAvailableMappings(type) {
  let allowedToMap = getAllowedToMapModels(type);
  let related = getIndirectlyMappedModels(type);
  let externalMap = getExternalMapModels(type);
  let allowedToCreate = getAllowedToCreateModels(type);

  return Object.assign({},
    allowedToMap, related, externalMap, allowedToCreate);
}

/**
 * Return grouped types.
 * @param {Array} types - array of base model types
 * @return {Array} - object with one allowed for mapping Model
 */
function groupTypes(types) {
  let groups = getTypeGroups();

  types.forEach((modelName) => {
    return _addFormattedType(modelName, groups);
  });

  _.forEach(groups, (group) => {
    group.items = _.sortBy(group.items, 'name');
  });

  return groups;
}

/**
 * Returns cmsModel fields in required format.
 * @param {can.Model} cmsModel - cms model
 * @return {object} - cms model in required format
 */
function _prepareCorrectTypeFormat(cmsModel) {
  return {
    category: cmsModel.category,
    name: cmsModel.title_plural,
    value: cmsModel.model_singular,
  };
}

/**
 * Adds model to correct group.
 * @param {string} modelName - model name
 * @param {object} groups - type groups
 */
function _addFormattedType(modelName, groups) {
  let cmsModel = getModelByType(modelName);
  if (!cmsModel || !cmsModel.title_singular) {
    return;
  }
  let type = _prepareCorrectTypeFormat(cmsModel);
  let group = !groups[type.category] ?
    groups.governance :
    groups[type.category];

  group.items.push(type);
}

/*
  return all allowed mappings (suitable for joining) for an object type.
  object - a string representing the object type's shortName

  return: a keyed object of all mappings (instances of Cacheable)
*/
function getAllowedToMapModels(object) {
  return _getModelsFromConfig(object, 'map');
}

/**
 * Returns collection of models allowed for unmapping
 * @param {String} object - the object type's shortName
 * @return {Object} a keyed object of allowed for unmapping models
 */
function getAllowedToUnmapModels(object) {
  return _getModelsFromConfig(object, 'unmap');
}

/**
 * Returns collection of models allowed for creating and mapping
 * @param {String} object - the object type's short name
 * @return {Object} - a keyed object of allowed for creating and mapping models
 */
function getAllowedToCreateModels(object) {
  return _getModelsFromConfig(object, 'create');
}

function _getModelsFromConfig(object, prop) {
  let mappings = {};
  if (config[object] && config[object][prop]) {
    _.forEach(config[object][prop],
      (model) => {
        mappings[model] = businessModels[model];
      });
  }
  return mappings;
}

/*
  return all possible indirectly mapped models for an object type.
  object - a string representing the object type's shortName

  return: a keyed object of all related mappings (instances of Cacheable)
*/
function getIndirectlyMappedModels(object) {
  return _getModelsFromConfig(object, 'indirectMappings');
}

/**
 * Returns object with models which can be mapped externally only
 * @param {string} object model name
 * @return {Object} allowed for external mapping models
 */
function getExternalMapModels(object) {
  return _getModelsFromConfig(object, 'externalMap');
}

function shouldBeMappedExternally(source, destination) {
  let externalMappings = getExternalMapModels(source);
  return _.keys(externalMappings).includes(destination);
}

export {
  getMappingList,
  allowedToCreate,
  allowedToMap,
  allowedToCreateOrMap,
  allowedToUnmap,
  getAllowedToUnmapModels,
  getAvailableMappings,
  groupTypes,
  shouldBeMappedExternally,
};

