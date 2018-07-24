/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';

  GGRC.Components('inlineFormControl', {
    tag: 'inline-form-control',
    viewModel: {
      deferredSave: null,
      instance: null,

      saveInlineForm: function (args) {
        let self = this;

        this.attr('deferredSave').push(function () {
          self.attr('instance.' + args.propName, args.value);
        }).fail(function (instance, xhr) {
          GGRC.Errors.notifierXHR('error')(xhr);
        });
      },
    },
  });
})(window.can);
