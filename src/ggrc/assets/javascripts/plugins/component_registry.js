
/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

(function (GGRC, can, _) {
  'use strict';

  if (_.isFunction(GGRC.Components)) {
    return;  // no need to create the component registry again
  }

  // make the registry publicly avilable
  GGRC.Components = Components;

  /**
   * An object representing the CanJS component registry.
   *
   * If invoked directly as a function, it creates a new component by
   * delegating the work to can.Component.extend(), and registers the resulting
   * constructor function under the given name.
   *
   * The name must be a nonempty string, and an error is thrown if the name has
   * already been taken.
   *
   * @param {String} name - the name under which to register the component
   * @param {Object} config - the component configuration object as expected
   *   by the underlying can.Component.extend() method
   *
   * @return {Function} - the created component constructor
   */
  function Components(name, config) {
    var constructor;

    if (!name || !_.isString(name)) {
      throw new Error('Component name must be a nonempty string.');
    }

    if (Components._registry[name]) {
      throw new Error('Component already exists: ' + name);
    }

    constructor = can.Component.extend(config);
    Components._registry[name] = constructor;

    return constructor;
  }

  // the internal storage of the registered components
  Components._registry = {};

  /**
   * Remove a registered component from the registry.
   *
   * If the component already does not exist, the function silently does
   * nothing.
   *
   * @param {String} name - the name of the component to deregister
   */
  Components.unregister = function (name) {
    delete Components._registry[name];
  };

  /**
   * Checks whether a component exists in the registry.
   *
   * @param {String} name - the name of the component
   * @return {Boolean} - true if the component exists, false false otherwise
   */
  Components.isRegistered = function (name) {
    return !_.isUndefined(Components._registry[name]);
  };

  /**
   * Retrieve a component from the registry.
   *
   * If the component is not found, an error is thrown.
   *
   * @param {String} name - the name of the component to retrieve
   * @return {Function} - the component's constructor function
   */
  Components.get = function (name) {
    var component = Components._registry[name];

    if (!component) {
      throw new Error('Component not found: ' + name);
    }

    return Components._registry[name];
  };
})(window.GGRC = window.GGRC || {}, can, _);
