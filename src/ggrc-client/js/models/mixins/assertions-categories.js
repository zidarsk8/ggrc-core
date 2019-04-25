/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';
import {isSnapshot} from '../../plugins/utils/snapshot-utils';

export default Mixin.extend({
  cleanupCollections(resource) {
    if (isSnapshot(this)) {
      return resource;
    }

    if (this.attr('categories')) {
      this.attr('categories').replace([]);
    }

    if (this.attr('assertions')) {
      this.attr('assertions').replace([]);
    }

    return resource;
  },
  'before:restore'() {
    this.cleanupCollections();
  },
});
