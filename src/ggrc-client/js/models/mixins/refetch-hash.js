/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';

/**
 * A mixin to generate hash with refetch param.
 */
export default Mixin.extend({
  getHashFragment: function () {
    let widgetName = this.constructor.table_singular;
    if (window.location.hash
      .startsWith(['#', widgetName].join(''))) {
      return;
    }

    return [widgetName,
      '&refetch=true'].join('');
  },
});
