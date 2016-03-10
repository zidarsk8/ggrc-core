/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (_) {
  _.mixin({
    exists: function (obj, key) {
      var keys;
      var slice = Array.prototype.slice;

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
    }
  });
})(_);
