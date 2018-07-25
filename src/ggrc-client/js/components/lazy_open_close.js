/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default can.Component.extend({
  tag: 'lazy-openclose',
  viewModel: {
    show: false,
  },
  init: function () {
    this._control.element.closest('.tree-item').find('.openclose')
      .bind('click', function () {
        this.viewModel.attr('show', true);
      }.bind(this));
  },
});
