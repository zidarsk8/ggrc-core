/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CustomAttributeObject from './custom-attribute-object';
import {CUSTOM_ATTRIBUTE_TYPE} from './custom-attribute-config';
import {
  hasGCAErrors,
} from '../../../plugins/utils/custom-attribute/custom-attribute-validations';

/**
 * @typedef {Object} CustomAttributeChange
 * @property {number} caId - The id for custom attribute which should be updated.
 * @property {(string|number|boolean)} value - Some value.
 */

/**
 * @typedef {Object} Options
 * @property {CUSTOM_ATTRIBUTE_TYPE} type - Type of custom attribute.
 */

/**
 * @class
 * @classdesc
 * Provides opportunity to manipulate custom attriubutes.
 */
export default class CustomAttributeAccess {
  /**
   * Creates CustomAttributeAccess instance.
   * @param {can.Map} instance - The instance of some object.
   */
  constructor(instance) {
    this._instance = instance;
    this._setupCaDefinitions();
    this._setupCaValues();
    this._setupCaObjects();
  }

  /**
   * Updates custom attribute with help [change]{@link CustomAttributeChange}.
   * @param {CustomAttributeChange} change - The custom attribute change.
   * @example
   * const change = {
   *    caId: 23,
   *    value: "Important text",
   * }
   *
   * access.write(change)
   */
  write(change) {
    const caObject = this._findCaObjectByCaId(change.caId);
    this._applyChangeToCaObject(caObject, change);
  }

  /**
   * Reads information about custom attributes.
   * @param {(Options|number|undefined)=} arg - Arg may be:
   *  undefined: Gives ability to return all custom attributes.
   *  Options: {@link Options} gives ability to filter custom attributes by
   *  certain rules.
   *  number: Gives ability to find the custom attriubte by passed custom attribute id.
   * @return {CustomAttributeObject|List<CustomAttributeObject>|undefined} - Custom
   *  attriubtes or ceratain custom attriubte.
   */
  read(arg) {
    if (!arg) {
      return this._caObjects;
    } else if (arg instanceof Object) {
      const options = arg;
      return this._getFilteredCaObjects(options);
    } else {
      const caId = arg;
      return this._findCaObjectByCaId(caId);
    }
  }

  /**
   * Builds custom attribute objects for the instance whiсh is served by
   * {@link CustomAttributeAccess}.
   * For each custom attribute object is set appopriate validations.
   * If the instance doesn't have appopriate custom attribute value for
   * custom attribute definition then is built the custom attribute
   * object with an empty custom attribute value.
   * @private
   */
  _setupCaObjects() {
    const instance = this._instance;
    const caDefinitions = instance.attr('custom_attribute_definitions');
    const caValues = instance.attr('custom_attribute_values');
    const caObjects = caDefinitions
      .map((caDefinition) => {
        const caId = caDefinition.attr('id');
        let caValue = this._findCaValueByCaId(caId);

        if (!caValue) {
          caValue = new can.Map({});
          caValues.push(caValue);
        }

        return new CustomAttributeObject(
          instance,
          caDefinition,
          caValue
        );
      });

    // set validate actions
    this._setupValidations(caObjects);
    // setup init validationState for each caObject
    _.each(caObjects, (caObject) => caObject.validate());
    this._caObjects = new can.List(caObjects);
  }

  /**
   * Sets for each [custom attribute object]{@link CustomAttributeObject}
   * appopriate validation.
   * @private
   * @param {can.List<CustomAttributeObject>} caObjects - Custom attribute objects.
   */
  _setupValidations(caObjects) {
    caObjects.each((caObject) => {
      this._buildDefaultValidations(caObject);
    });
  }

  /**
   * Builds default validations for Local
   * [caObject]{@link CustomAttributeObject}.
   * @private
   * @param {CustomAttributeObject} caObject - The custom attribute object for
   * which is set validations.
   */
  _buildDefaultValidations(caObject) {
    const validator = caObject.validator;
    validator.addValidationActions(hasGCAErrors);
  }

  /**
   * Returns filtered custom attribute objects by certain type.
   * @param {Options} options - {@link Options}.
   * @param {can.List<CUSTOM_ATTRIBUTE_TYPE>} [options.type=CUSTOM_ATTRIBUTE_TYPE.GLOBAL] -
   *  {@link CUSTOM_ATTRIBUTE_TYPE}.
   * @return {can.List<CustomAttributeObject>} - Filtered custom attribute objects.
   */
  _getFilteredCaObjects({type = CUSTOM_ATTRIBUTE_TYPE.GLOBAL}) {
    const caObjects = this._caObjects;
    return caObjects.filter((caObject) => caObject.type === type);
  }

  /**
   * Setups custom_attribute_values field for the instance.
   */
  _setupCaValues() {
    const instance = this._instance;

    if (!instance.attr('custom_attribute_values')) {
      instance.attr('custom_attribute_values', []);
    }
  }

  /**
   * Setups custom_attribute_definitions field for the instance.
   */
  _setupCaDefinitions() {
    const instance = this._instance;
    let caDefs = instance.attr('custom_attribute_definitions');

    if (!caDefs) {
      // get all global custom attributes for instance
      const definitionType = instance.constructor.root_object;
      caDefs = this._getGlobalCustomAttributes(definitionType);
    }

    instance.attr('custom_attribute_definitions', caDefs);
  }

  /**
   * Returns global custom attriubtes for certain definitionType.
   * @param {string} definitionType - The name of the definition type.
   * @example
   *  definitionType = "objective"
   * @return {Object[]} - Global custom attriubtes.
   */
  _getGlobalCustomAttributes(definitionType) { // eslint-disable-line
    return GGRC.custom_attr_defs.filter((gca) =>
      gca.definition_type === definitionType &&
      gca.definition_id === null
    );
  }

  /**
   * Applies [change]{@link CustomAttributeChange} to [custom attribute object]
   * {@link CustomAttributeObject}.
   * @param {CustomAttributeObject} caObject - The custom attribute object.
   * @param {CustomAttributeChange} change - The custom attribute change.
   */
  _applyChangeToCaObject(caObject, {value}) {
    caObject.value = value;
  }

  /**
   * Returns custom attribute value object which equals to сaId.
   * @param {number} caId - The custom attribute id.
   * @return {can.Map|undefined} - Custom attribute value if it was found
   * else undefined.
   */
  _findCaValueByCaId(caId) {
    const instance = this._instance;
    const caValues = instance.attr('custom_attribute_values');
    return _.find(caValues, (caValue) =>
      caValue.attr('custom_attribute_id') === caId
    );
  }

  /**
   * Returns [custom attribute object]{@link CustomAttributeObject} which
   * has certain сaId.
   * @param {number} caId - The custom attribute id.
   * @return {CustomAttributeObject|undefined} - Custom attribute object if it
   * was found else undefined.
   */
  _findCaObjectByCaId(caId) {
    const caObjects = this._caObjects;
    return _.find(caObjects, (caObject) =>
      caObject.customAttributeId === caId
    );
  }
}
