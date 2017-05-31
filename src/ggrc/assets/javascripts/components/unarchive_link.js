/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  can.Component.extend({
    tag: 'unarchive-link',
    scope: {
      notify: '@',
      instance: null,
      notifyText: 'was unarchived successfully'
    },
    template: ['<a href="#">',
               '<content></content>',
               '</a>'].join(''),
    events: {
      'a click': function (el, event) {
        var instance = this.scope.attr('instance');
        var notifyText = this.scope.attr('instance.title') + ' ' +
          this.scope.attr('notifyText');

        event.preventDefault();

        if (instance && instance.archived) {
          instance.archived = false;
          instance.save()
            .then(function () {
              if (this.scope.attr('notify')) {
                $('body').trigger('ajax:flash', {success: notifyText});
              }
            }.bind(this));
        }
      }
    }
  });
})(window.can, window.can.$);
