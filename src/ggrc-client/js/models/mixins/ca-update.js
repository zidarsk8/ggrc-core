/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';

export default class CaUpdate extends Mixin {
  after_save() {
    this.dispatch('readyForRender');
  }

  info_pane_preload() {
    this.refresh();
  }
}
