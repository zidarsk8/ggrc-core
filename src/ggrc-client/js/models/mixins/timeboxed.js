/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';

/**
 * A mixin to use for objects that can have a time limit imposed on them.
 */
export default Mixin.extend({
  'extend:attributes': {
    start_date: 'date',
    end_date: 'date',
  },

  // Override default CanJS's conversion/serialization of dates, because
  // that takes the browser's local timezone into account, which we do not
  // want with our UTC dates. Having plain UTC-formatted date strings is
  // more suitable for the current structure of the app.
  serialize: {
    date: function (val, type) {
      return val;
    },
  },

  convert: {
    date: function (val, oldVal, fn, type) {
      return val;
    },
  },
}, {});
