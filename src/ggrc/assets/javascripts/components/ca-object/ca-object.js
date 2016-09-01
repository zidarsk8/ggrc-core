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
      update: function (value) {
        this.attr('value', value);
        this.attr('isModified', this.attr('def.id'));
      },
      save: function (value) {
        var instance = this.attr('instance');
        var type = this.attr('type');

        this.attr('isSaving', true);

        this.update(value, type);
        instance.save()
          .done(function () {
            can.$(document.body).trigger('ajax:flash', {
              success: 'Saved'
            });
          })
          .fail(function (instance, err) {
            GGRC.Errors.notifier()(err);
          })
          .always(function () {
            this.attr('isSaving', false);
          }.bind(this));
      }
    },
    events: {
      '{scope} value': function (scope, ev, val) {
        this.scope.save(val);
      }
    }
  });
})(window._, window.can, window.GGRC);
