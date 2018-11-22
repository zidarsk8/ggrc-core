/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getModelByType} from '../../plugins/utils/models-utils';
import * as businessModels from '../business-models';
import Permission from '../../permission';
import TreeViewConfig from '../../apps/base_widgets';

/*
  class Mappings
  represents everything known about how GGRC objects connect to each other.

  a Mappings instance contains the set of known mappings.
  The set of all Mappings instances is used throughout the
  system to build widgets, map and unmap objects, etc.

  To configure a new Mappings instance, use the following format :
  { <source object type> : {
      map : [ <object name>, ...]
      <mapping name> : Proxy(...) | Direct(...)
                      | Multi(...)
                      | CustomFilter(...),
      ...
    }
  }
*/
export default can.Construct.extend({
  config: null,
  getTypeGroups: function () {
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
  },

  /**
   * Return list of allowed for mapping models.
   * Performs checks for
   * @param {String} type - base model type
   * @param {Array} include - array of included models
   * @param {Array} exclude - array of excluded models
   * @return {Array} - list of allowed for mapping Models
   */
  getMappingList: function (type) {
    if (!type) {
      return [];
    }

    let allowedToMap = this.getAllowedToMapModels(type);
    let list = TreeViewConfig.attr('base_widgets_by_type')[type];
    const compacted = _.compact([_.keys(allowedToMap), list]);
    return _.intersection(...compacted);
  },
  /**
   * Determine if two types of models can be mapped
   *
   * @param {String} target - the target type of model
   * @param {String} source - the source type of model
   *
   * @return {Boolean} - true if mapping is allowed, false otherwise
   */
  isMappableType: function (target, source) {
    let result;
    if (!target || !source) {
      return false;
    }
    result = this.getMappingList(target);
    return _.includes(result, source);
  },
  /**
   * Determine if `source` is allowed to be mapped to `target`.
   *
   * By symmetry, this method can be also used to check whether `source` can
   * be unmapped from `target`.
   *
   * @param {Object} source - the source object the mapping
   * @param {Object} target - the target object of the mapping
   * @param {Object} options - the options objects, similar to the one that is
   *   passed as an argument to Mustache helpers
   *
   * @return {Boolean} - true if mapping is allowed, false otherwise
   */
  allowedToMap: function (source, target, options) {
    let canMap = false;
    let types;
    let targetType;
    let sourceType;
    let targetContext;
    let sourceContext;
    let createContexts;

    const MAPPING_RULES = Object.freeze({
      // mapping audit and assessment to issue is not allowed,
      // but unmap can be possible
      'issue audit': (options && options.isIssueUnmap),
      'issue assessment': (options && options.isIssueUnmap),
    });

    targetType = this._getType(target);
    sourceType = this._getType(source);
    types = [sourceType.toLowerCase(), targetType.toLowerCase()];

    // special check for snapshot:
    if (options &&
      options.context &&
      options.context.parent_instance &&
      options.context.parent_instance.snapshot) {
      // Avoid add mapping for snapshot
      return false;
    }

    let oneWayProp = types.join(' ');
    if (MAPPING_RULES.hasOwnProperty(oneWayProp)) {
      // One-way check
      // special case check:
      // - mapping an Audit and Assessment to a Issue is not allowed
      // (but vice versa is allowed)
      return MAPPING_RULES[oneWayProp];
    } else {
      if (!this.isMappableType(sourceType, targetType)) {
        return false;
      }
    }

    targetContext = _.exists(target, 'context.id');
    sourceContext = _.exists(source, 'context.id');
    createContexts = _.exists(
      GGRC, 'permissions.create.Relationship.contexts');

    canMap = Permission.is_allowed_for('update', source) ||
      _.includes(createContexts, sourceContext) ||
      // Also allow mapping to source if the source is about to be created.
      _.isUndefined(source.created_at);

    if (target instanceof can.Map && targetType) {
      canMap = canMap &&
        (Permission.is_allowed_for('update', target) ||
          _.includes(createContexts, targetContext));
    }
    return canMap;
  },
  _getType: function (object) {
    let type;

    if (object instanceof can.Model) {
      type = object.constructor.shortName;
    } else {
      type = object.type || object;
    }

    if (type === 'Snapshot') {
      type = object.child_type; // check Snapshot original object type
    }

    return type;
  },
  /**
   * Return list of allowed for mapping types.
   * Performs checks for
   * @param {String} type - base model type
   * @return {Array} - list of allowed for mapping Models
   */
  getMappingTypes: function (type) {
    let list = this.getMappingList(type);
    return this.groupTypes(list);
  },
  /**
   * Return allowed for mapping type in appropriate group.
   * @param {String} type - base model type
   * @return {Array} - object with one allowed for mapping Model
   */
  getMappingType: function (type) {
    return this.groupTypes([type]);
  },
  /**
   * Returns the list of allowed direct mapping models
   * with possible related mapping models
   * @param {String} type - base model type
   * @return {Array} - list of available mappings
   */
  getAvailableMappings(type) {
    let allowedToMap = this.getAllowedToMapModels(type);
    let related = this.getIndirectlyMappedModels(type);

    return Object.assign({}, allowedToMap, related);
  },
  /**
   * Return grouped types.
   * @param {Array} types - array of base model types
   * @return {Array} - object with one allowed for mapping Model
   */
  groupTypes(types) {
    let groups = this.getTypeGroups();

    types.forEach((modelName) => {
      return this._addFormattedType(modelName, groups);
    });

    _.forEach(groups, (group) => {
      group.items = _.sortBy(group.items, 'name');
    });

    return groups;
  },
  /**
   * Returns cmsModel fields in required format.
   * @param {can.Model} cmsModel - cms model
   * @return {object} - cms model in required format
   */
  _prepareCorrectTypeFormat: function (cmsModel) {
    return {
      category: cmsModel.category,
      name: cmsModel.title_plural,
      value: cmsModel.model_singular,
      singular: cmsModel.model_singular,
      plural: cmsModel.title_plural.toLowerCase().replace(/\s+/, '_'),
    };
  },
  /**
   * Adds model to correct group.
   * @param {string} modelName - model name
   * @param {object} groups - type groups
   */
  _addFormattedType: function (modelName, groups) {
    let group;
    let type;
    let cmsModel;
    cmsModel = getModelByType(modelName);
    if (!cmsModel || !cmsModel.title_singular) {
      return;
    }
    type = this._prepareCorrectTypeFormat(cmsModel);
    group = !groups[type.category] ?
      groups.governance :
      groups[type.category];

    group.items.push(type);
  },
  /*
    return all mappings for an object type.
    object - a string representing the object type's shortName

    return: a keyed object of all mappings (instances of GGRC.ListLoaders.BaseListLoader) by mapping name
    Example: Mappings.get_mappings_for('Program')
  */
  get_mappings_for: function (object) {
    let mappings = {};
    if (this.config[object]) {
      _.forEach(this.config[object], function (mapping, mappingName) {
        if (mappingName === 'map') {
          return;
        }
        mappings[mappingName] = mapping;
      });
    }
    return mappings;
  },
  /*
    return all allowed mappings (suitable for joining) for an object type.
    object - a string representing the object type's shortName

    return: a keyed object of all mappings (instances of CMS.Models)
  */
  getAllowedToMapModels: function (object) {
    return this._getModelsFromConfig(object, 'map');
  },
  _getModelsFromConfig(object, prop) {
    let mappings = {};
    let config = this.config;
    if (config[object] && config[object][prop]) {
      _.forEach(config[object][prop],
        (model) => {
          mappings[model] = businessModels[model];
        });
    }
    return mappings;
  },
  get_mapper: function (mappingName, type) {
    let mapper;
    let mappers = this.get_mappings_for(type);
    if (mappers) {
      mapper = mappers[mappingName];
      return mapper;
    }
  },
  _get_binding_attr: function (mapper) {
    if (typeof (mapper) === 'string') {
      return '_' + mapper + '_binding';
    }
  },
  // checks if binding exists without throwing debug statements
  // modeled after what get_binding is doing
  has_binding: function (mapper, model) {
    let binding;
    let mapping;
    let bindingAttr = this._get_binding_attr(mapper);

    if (bindingAttr) {
      binding = model[bindingAttr];
    }

    if (!binding) {
      if (typeof (mapper) === 'string') {
        mapping = this.get_mapper(mapper, model.constructor.shortName);
        if (!mapping) {
          return false;
        }
      } else if (!(mapper instanceof GGRC.ListLoaders.BaseListLoader)) {
        return false;
      }
    }

    return true;
  },
  get_binding: function (mapper, model) {
    let mapping;
    let binding;
    let bindingAttr = this._get_binding_attr(mapper);

    if (bindingAttr) {
      binding = model[bindingAttr];
    }

    if (!binding) {
      if (typeof (mapper) === 'string') {
      // Lookup and attach named mapper
        mapping = this.get_mapper(mapper, model.constructor.shortName);
        if (!mapping) {
          console.warn(
            `No such mapper: ${model.constructor.shortName}.${mapper}`);
        } else {
          binding = mapping.attach(model);
        }
      } else if (mapper instanceof GGRC.ListLoaders.BaseListLoader) {
      // Loader directly provided, so just attach
        binding = mapper.attach(model);
      } else {
        console.warn(`Invalid mapper specified: ${mapper}`);
      }
      if (binding && bindingAttr) {
        model[bindingAttr] = binding;
        binding.name = model.constructor.shortName + '.' + mapper;
      }
    }
    return binding;
  },
  get_list_loader: function (name, model) {
    let binding = this.get_binding(name, model);
    return binding.refresh_list();
  },
  /*
    return all possible indirectly mapped models for an object type.
    object - a string representing the object type's shortName

    return: a keyed object of all related mappings (instances of CMS.Models)
  */
  getIndirectlyMappedModels(object) {
    return this._getModelsFromConfig(object, 'indirectMappings');
  },
}, {
  init: function (definitions) {
    if (this.constructor.config) {
      throw new Error('Mappings are already initialized.');
    }

    this.constructor.config = definitions;
  },
});
