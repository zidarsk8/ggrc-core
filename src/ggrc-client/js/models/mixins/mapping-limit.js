/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';

export default Mixin('mapping-limit', {
  getAllowedMappings() {
    return _.union(
      GGRC.config.snapshotable_objects,
      ['Issue']
    );
  },
}, {});
