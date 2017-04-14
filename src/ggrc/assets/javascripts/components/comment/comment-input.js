/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tag = 'comment-input';
  var template = can.view(GGRC.mustache_path +
    '/components/comment/comment-input.mustache');

  GGRC.Components('commentInput', {
    tag: tag,
    template: template,
    viewModel: {
      define: {
        disabled: {
          type: 'boolean',
          value: false
        },
        placeholder: {
          type: 'string',
          value: ''
        },
        isEmpty: {
          type: 'boolean',
          value: true,
          get: function () {
            var value = this.attr('value') || '';
            return !value.length;
          }
        },
        clean: {
          type: 'boolean',
          value: true,
          set: function (newValue) {
            if (newValue) {
              this.attr('value', '');
            }
            return newValue;
          }
        },
        value: {
          type: 'string',
          value: '',
          set: function (newValue) {
            return newValue || '';
          }
        }
      }
    }
  });
})(window.can, window.GGRC);
