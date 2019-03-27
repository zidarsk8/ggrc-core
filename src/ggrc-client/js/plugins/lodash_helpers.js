/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (_) {
  _.mixin({
    exists: function (obj, key) {
      let keys;
      let slice = Array.prototype.slice;

      if (!key) {
        return obj;
      }
      if (arguments.length > 2) {
        keys = slice.call(arguments).slice(1);
      } else {
        keys = key.split('.');
      }
      return keys.reduce(function (base, memo) {
        return (_.isUndefined(base) || _.isNull(base)) ? base : base[memo];
      }, obj);
    },
    /*
     * Splits string into array and trims its values
     *
     * @param {String} values - Input string that should be manipulated
     * @param {String} splitter - String that is used to split `values`
     *                            - Default splitter is comma - `,`
     * @param {Object} options - Additional options
     *                           - Unique - returns only unique values
     *                           - Compact - removes `falsy` values
     * @return {Array} - Returns array of splited values
     */
    splitTrim: function (values, splitter, options) {
      if (!values || !values.length) {
        return [];
      }
      if (_.isUndefined(splitter)) {
        splitter = ',';
      }
      if (_.isObject(splitter)) {
        options = splitter;
        splitter = ',';
      }

      values = values.split(splitter);
      values = _.map(values, _.trim);

      options = options || {};
      if (options.unique) {
        values = _.uniq(values);
      }
      if (options.compact) {
        values = _.compact(values);
      }
      return values;
    },
    /*
     * Get array of keys that are truthy
     *
     * @param {Object} object - Object with key - values
     * @return {Array} - Returns array of truthy keys
     */
    getExistingKeys: function (object) {
      return _.keys(_.pickBy(object, _.identity));
    },

    /**
     *
     * @param {Array} items - array of items.
     * @param {Function} predicate - function with the condition for "map" operation
     * @return {Array} - result of "map" operation without "null" and "undefined" values
     */
    filteredMap: function (items, predicate) {
      return _.map(items, predicate)
        .filter((item) => !_.isNull(item) && !_.isUndefined(item));
    },
  });
})(_);
