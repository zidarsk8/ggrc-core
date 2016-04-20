/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: urban@reciprocitylabs.com
 Maintained By: urban@reciprocitylabs.com
 */
(function (can, $) {
  GGRC.Components('reminder', {
    tag: 'reminder',
    template: '<content/>',
    scope: {
      instance: null,
      type: '@',
      modal_title: '@',
      modal_description: '@',
      reminder: function (scope, el, ev) {
        var instance = scope.instance;

        instance.refresh();
        instance.attr('reminderType', scope.type);

        $.when(instance.save()).then(function () {
          GGRC.Controllers.Modals.confirm({
            modal_title: scope.attr('modal_title'),
            modal_description: scope.attr('modal_description'),
            button_view: GGRC.mustache_path + '/modals/close_buttons.mustache'
          });
        });
      }
    }
  });
})(window.can, window.can.$);
