
/*!
  Copyright (C) 2016 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can, _) {
  'use strict';

  if (_.isFunction(GGRC.Components)) {
    return;  // no need to create the component registry again
  }

  // make the registry publicly available
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
    var definitions;

    if (!name || !_.isString(name)) {
      throw new Error('Component name must be a nonempty string.');
    }

    if (Components._registry[name]) {
      throw new Error('Component already exists: ' + name);
    }

    if (config.scope && _.isObject(config.scope.define)) {
      definitions = config.scope.define;
      delete config.scope.define;
    }

    if (definitions) {
      config.init = Components._extendInit(config.init, definitions);
    }

    constructor = can.Component.extend(config);
    Components._registry[name] = constructor;

    return constructor;
  }

  /**
   * Wrap component init function
   *
   * @param {Function} init - Component init function
   * @param {Object} definitions - Type definitions and their defaults
   *
   * @return {Function} - Returns wrapped init function
   */
  Components._extendInit = function (init, definitions) {
    init = init || $.noop;

    return function (element, options) {
      var scope = this.scope;
      var val;

      _.each(definitions, function (obj, key) {
        var prefix = '';
        if (!_.has(scope, key)) {
          if (obj.type === 'function') {
            prefix = 'can-';
          }
          val = element.getAttribute(prefix + can.camelCaseToDashCase(key));
          val = Components._castValue(val, obj.type, options);
          if (_.isUndefined(val) && _.has(obj, 'default')) {
            val = obj.default;
          }
          scope.attr(key, val);
        }
      }, this);

      return init.call(this, arguments);
    };
  };

  /**
   * Cast scope values for default types
   *
   * @param {String} val - Value we get from element attribute
   * @param {String} type - Type for the value we need to get
   * @param {object} options - init function options
   *
   * @return {Any} - Returns casted types
   */
  Components._castValue = function (val, type, options) {
    var types = {
      'boolean': function (bool) {
        if (_.isBoolean(bool)) {
          return bool;
        }
        return bool === 'true';
      },
      string: function (str) {
        if (_.isString(str)) {
          return str;
        }
        if (_.isEmpty(str)) {
          return;
        }
        return String(str);
      },
      number: function (num) {
        if (_.isNumber(num)) {
          return num;
        }
        num = parseInt(num, 10);
        if (_.isNaN(num)) {
          return;
        }
        return num;
      },
      'function': function (fn, options) {
        if (!fn || !options.scope.attr(fn)) {
          return;
        }
        return options.scope.attr(fn);
      }
    };
    if (!types[type]) {
      console.warn('Cast value for `' + type + '` is not defined');
      return undefined;
    }
    if (val &&
        type !== 'function' &&
        options.scope.attr(val)) {
      val = options.scope.attr(val);
    }
    return types[type](val, options);
  };

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
