/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';

export default class UniqueTitle extends Mixin {
  save_error(val) {
    if (/title values must be unique\.$/.test(val)) {
      this.attr('_transient_title', val);
    }
  }

  after_save() {
    this.removeAttr('_transient_title');
  }

  'before:attr'(key, val) {
    if (key === 'title' &&
      arguments.length > 1 &&
      this._transient) {
      this.attr('_transient_title', null);
    }
  }
}
