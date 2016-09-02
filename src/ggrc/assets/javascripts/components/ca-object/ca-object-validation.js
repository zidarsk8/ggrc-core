/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/ca-object/ca-object-validation.mustache');

  GGRC.Components('сustomAttributeObjectValidation', {
    tag: 'ca-object-validation',
    template: tpl,
    scope: {
      valueId: '@',
      def: null,
      errors: null,
      value: null,
      isModified: null,
      validation: {},
      isEmpty: function () {
        var errors = this.attr('errors');
        return errors.length && this.hasError(errors, 'value');
      },
      hasError: function (errors, field) {
        return errors.indexOf(field) > -1;
      },
      isValid: function () {
        var errors = this.attr('errors');
        var requireComment = this.hasError(errors, 'comment');
        var requireEvidence = this.hasError(errors, 'evidence');
        return !(requireComment || requireEvidence);
      },
      setValidation: function () {
        this.attr('validation', {
          mandatory: this.attr('def.mandatory'),
          empty: this.isEmpty(),
          valid: this.isValid()
        });
      },
      checkRequired: function () {
        var isModified = this.attr('isModified');
        if (isModified && isModified === this.attr('def').id) {
          if (!this.isValid()) {
            this.setRequired(this.attr('errors').serialize());
          }
        }
      },
      setRequired: function (fields) {
        can.batch.start();
        this.attr('modal', {
          content: {
            value: this.attr('value'),
            title: this.attr('def.title'),
            type: this.attr('type')
          },
          caIds: {
            defId: this.attr('def.id'),
            valueId: parseInt(this.attr('valueId'), 10)
          },
          modalTitleText: 'Required ' + fields.map(function (field) {
            return can.capitalize(field);
          }).join(' and '),
          fields: fields
        });
        can.batch.stop();
        this.attr('isModified', null);
        this.attr('modal.open', true);
      }
    },
    events: {
      init: function () {
        this.scope.setValidation();
        this.scope.checkRequired();
      }
    }
  });
})(window._, window.can, window.GGRC);
