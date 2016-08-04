/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var cmpName = 'validation-icon';
  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/validation-icon.mustache');
  var tag = 'assessment-' + cmpName;
  /**
   * State object to present possible icons for validation
   */
  var icons = {
    noValidation: 'fa-check-circle',
    empty: 'fa-times-circle validation-icon-empty',
    valid: 'fa-check-circle validation-icon-valid',
    invalid: 'fa-times-circle validation-icon-invalid'
  };

  /**
   * Assessment specific validation icon component
   */
  GGRC.Components('assessmentValidationIcon', {
    tag: tag,
    template: tpl,
    scope: {
      caId: null,
      instance: null,
      validation: null,
      iconCls: icons.noValidation,
      applyState: function () {
        var icon = icons.noValidation;

        if (this.attr('validation.mandatory')) {
          icon = this.attr('validation.empty') ? icons.empty : icons.valid;
        }
        /* This validation is required for DropDowns with required attachments */
        if (!this.attr('validation.valid')) {
          icon = icons.invalid;
        }

        this.attr('iconCls', icon);
      },
      hasRequiredAttachments: function (attachments) {
        var id = parseInt(this.attr('caId'), 10);
        return attachments.every(function (x) {
          return x !== id;
        });
      },
      validate: function (list) {
        this.attr('validation.valid', this.hasRequiredAttachments(list));
      }
    },
    events: {
      init: function () {
        this.scope.applyState();
      },
      '{scope.validation} change': function () {
        this.scope.applyState();
      },
      '{scope.instance} invalidCustomAttributes': function (scope, ev, list) {
        this.scope.validate(list);
      }
    }
  });
})(window.can, window.GGRC);
