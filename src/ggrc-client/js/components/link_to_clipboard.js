/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Clipboard from 'clipboard';

export default can.Component.extend({
  tag: 'clipboard-link',
  viewModel: {
    text: '@',
    title: '@',
    notify: '@',
    isActive: false,
    timeout: '@',
    notifyText: 'Link has been copied to your clipboard.',
  },
  template: ['<a data-clipboard-text="{{text}}" {{#isActive}}class="active"{{/isActive}} href="#">',
    '<i class="fa fa-link"></i> {{title}}',
    '</a>'].join(''),
  events: {
    'a click': function (el, evnt) {
      evnt.preventDefault();
    },
    'inserted': function (el, evnt) {
      let timeout = this.viewModel.attr('timeout') || 10000;
      this._clip = new Clipboard(el.find('a')[0]);

      this._clip.on('success', function () {
        if (this.viewModel.attr('notify')) {
          $('body').trigger('ajax:flash', {'success': this.viewModel.attr('notifyText')});
        }
        this.viewModel.attr('isActive', true);
        setTimeout(function () {
          this.viewModel.attr('isActive', false);
        }.bind(this), timeout);
      }.bind(this));
    },
  },
});
