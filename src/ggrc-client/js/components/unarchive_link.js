/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, $) {
  'use strict';

  GGRC.Components('unarchiveLink', {
    tag: 'unarchive-link',
    scope: {
      notify: '@',
      instance: null,
      notifyText: 'was unarchived successfully',
    },
    template: ['<a href="#">',
      '<content></content>',
      '</a>'].join(''),
    events: {
      'a click': function (el, event) {
        let instance = this.scope.attr('instance');
        let notifyText = instance.display_name() + ' ' +
          this.scope.attr('notifyText');

        event.preventDefault();

        if (instance && instance.attr('archived')) {
          instance.attr('archived', false);
          instance.save()
            .then(function () {
              if (this.scope.attr('notify')) {
                $('body').trigger('ajax:flash', {success: notifyText});
              }
            }.bind(this));
        }
      },
    },
  });
})(window.GGRC, window.can.$);
