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
    scope: {
      placeholder: '@',
      disabled: false,
      clean: false,
      isEmpty: true,
      value: '',
      input: {
        placeholder: '',
        value: ''
      },
      setDisabled: function (isDisabled) {
        this.attr('disabled', isDisabled);
      },
      /**
       * Updates values of the component on modifications of the input of the Rich Text Editor
       * @param {String|null} value - Value received from the Rich Text Editor
       */
      setValues: function (value) {
        this.attr('value', value);
        this.attr('isEmpty', !(value && value.length));
      },
      initValues: function () {
        // Comment Input by default is empty
        this.attr('isEmpty', true);
        this.attr('input.placeholder', this.attr('placeholder') || '');
        this.attr('input.value', this.attr('value'));
      },
      performCleanup: function () {
        this.attr('input.value', null);
      }
    },
    events: {
      init: function () {
        this.scope.performCleanup();
        // Set default values
        this.scope.initValues();
      },
      '{scope} disabled': function (scope, ev, isDisabled) {
        this.scope.setDisabled(isDisabled);
      },
      '{scope.input} value': function (scope, ev, value) {
        this.scope.setValues(value);
      },
      '{scope} clean': function (scope, ev, doCleaning) {
        if (doCleaning) {
          this.scope.performCleanup();
        }
      }
    }
  });
})(window.can, window.GGRC);
