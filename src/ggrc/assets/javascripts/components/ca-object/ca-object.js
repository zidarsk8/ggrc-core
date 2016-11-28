/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/ca-object/ca-object.mustache');

  GGRC.Components('customAttributesObject', {
    tag: 'ca-object',
    template: tpl,
    scope: {
      instance: null,
      isModified: null,
      valueId: '@',
      value: null,
      type: null,
      def: null,
      isSaving: false,
      addComment: function () {
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
          modalTitleText: 'Add comment',
          fields: ['comment']
        });
        can.batch.stop();

        this.attr('modal.open', true);
      },
      setModified: function () {
        this.attr('isModified', this.attr('def.id'));
      },
      save: function () {
        var value = this.attr('value');
        this.setModified();
        this.attr('instance').save()
          .done(function () {
            // TODO: remove hack for flash message appearance after normal solution will be applied
            if (String(value) === this.attr('value')) {
              can.$(document.body).trigger('ajax:flash', {
                success: 'Saved'
              });
            }
          }.bind(this))
          .fail(function (inst, err) {
            GGRC.Errors.notifierXHR('error')(err);
          })
          .always(function () {
            this.attr('isSaving', false);
          }.bind(this));
      }
    },
    events: {
      '{scope} isSaving': function (scope, ev, isSaving) {
        if (isSaving) {
          scope.save();
        }
      }
    }
  });
})(window._, window.can, window.GGRC);
