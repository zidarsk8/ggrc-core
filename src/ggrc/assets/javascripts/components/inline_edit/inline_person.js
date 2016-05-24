/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  'use strict';

  GGRC.Components('inlinePerson', {
    tag: 'inline-person',
    template: can.view(
      GGRC.mustache_path +
      '/components/inline_edit/person.mustache'
    ),
    scope: {
      setPerson: function (scope, el, ev) {
        this.attr('context.value', ev.selectedItem.serialize());
      },
      unsetPerson: function (scope, el, ev) {
        ev.preventDefault();
        this.attr('context.value', undefined);
      }
    }
  });
})(window.can, window.can.$);
