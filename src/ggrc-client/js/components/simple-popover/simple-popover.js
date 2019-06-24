/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './simple-popover.stache';

export default CanComponent.extend({
  tag: 'simple-popover',
  view: can.stache(template),
  init: function (el) {
    this.viewModel.attr('element', el);
  },
  leakScope: true,
  viewModel: CanMap.extend({
    extraCssClass: '',
    placement: '',
    buttonText: '',
    open: false,
    show: function () {
      this.attr('open', true);
      document.addEventListener('mousedown', this);
    },
    hide: function () {
      this.attr('open', false);
      document.removeEventListener('mousedown', this);
    },
    toggle: function () {
      this.attr('open') ? this.hide() : this.show();
    },
    handleEvent: function (event) {
      if (this.attr('element')
        && !this.attr('element').contains(event.target)) {
        this.hide();
      }
    },
  }),
  events: {
    removed: function () {
      document.removeEventListener('mousedown', this.viewModel);
    },
  },
});
