/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  GGRC.Components('textarea-array', {
    tag: 'textarea-array',
    template:
      '<textarea class="{{className}}" placeholder="{{placeholder}}">' +
      '{{content}}' +
      '</textarea>',
    scope: {
      array: null,
      className: '@',
      delimeter: ', ',
      placeholder: '@',
      init: function () {
        this.updateContent();
      },
      updateContent: function () {
        let array = this.attr('array') || [];
        this.attr('content', array.join(this.attr('delimeter')));
      }
    },
    events: {
      'textarea change': function (el, ev) {
        let val = $(el).val();
        this.scope.attr('array',
          $.map(val.split(','), $.proxy(''.trim.call, ''.trim)));
        this.scope.updateContent();
      }
    }
  });
})(window.can);
