/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  var icons = {
    noValidation: 'fa-check-circle',
    empty: 'fa-times-circle validation-icon-empty',
    valid: 'fa-check-circle validation-icon-valid',
    invalid: 'fa-times-circle validation-icon-invalid'
  };

  var titles = {
    noValidation: ' ',
    empty: 'validation-title-empty',
    valid: 'validation-title-valid',
    invalid: 'validation-title-invalid'
  };

  can.Component.extend({
    tag: 'ca-object',
    viewModel: {
      define: {
        validation: {},
        iconCls: {
          value: icons.noValidation,
          get: function () {
            var icon = icons.noValidation;

            if (this.attr('validation.mandatory')) {
              icon = this.attr('validation.empty') ? icons.empty : icons.valid;
            }
            /* This validation is required for DropDowns with required attachments */
            if (!this.attr('validation.valid')) {
              icon = icons.invalid;
            }
            return icon;
          }
        },
        titleCls: {
          value: titles.noValidation,
          get: function () {
            var icon = titles.noValidation;

            if (this.attr('validation.mandatory')) {
              icon = this.attr('validation.empty') ?
                                      titles.empty :
                                      titles.valid;
            }
            /* This validation is required for DropDowns with required attachments */
            if (!this.attr('validation.valid')) {
              icon = titles.invalid;
            }
            return icon;
          }
        }
      },
      valueId: null,
      value: null,
      type: null,
      def: null,
      isSaving: false,
      addComment: function () {
        can.batch.start();
        this.attr('modal', {
          content: {
            fields: ['comment'],
            value: this.attr('value'),
            title: this.attr('def.title'),
            type: this.attr('type')
          },
          caIds: {
            defId: this.attr('def.id'),
            valueId: this.attr('valueId')
          },
          modalTitle: 'Add comment',
          state: {}
        });
        can.batch.stop();

        this.attr('modal.state.open', true);
      }
    },
    events: {
      '{viewModel} isSaving': function (scope, ev, isSaving) {
        if (isSaving) {
          this.element.trigger('saveCustomAttribute', [scope]);
        }
      }
    }
  });
})(window.can);
