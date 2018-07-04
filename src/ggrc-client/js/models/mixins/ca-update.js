/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';

export default Mixin('ca_update', {}, {
  after_save: function () {
    this.dispatch('readyForRender');
  },
  info_pane_preload: function () {
    this.refresh();
  },
});
