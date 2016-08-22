/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/ca-object/ca-object.mustache');

  function mapValueFromCA(value, type) {
    if (type === 'checkbox') {
      return value === '1';
    }
    if (type === 'person') {
      if (value && value instanceof can.Map) {
        return value.serialize();
      }
      return _.isEmpty(value) ? undefined : value;
    }

    if (type === 'dropdown') {
      if (_.isNull(value) || _.isUndefined(value)) {
        return '';
      }
    }
    return value;
  }

  function mapValuesToCA(value, type) {
    if (type === 'checkbox') {
      return value ? 1 : 0;
    }

    if (type === 'person') {
      if (value && value instanceof can.Map) {
        return 'Person:' + value.id;
      }
      return _.isEmpty(value) ? undefined : value;
    }
    return value;
  }

  GGRC.Components('customAttributesObject', {
    tag: 'ca-object',
    template: tpl,
    scope: {
      instance: null,
      input: {
        value: null,
        type: null,
        options: [],
        placeholder: 'Please enter the value...'
      },
      isModified: null,
      valueId: '@',
      value: null,
      valueObj: null,
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
      getOptions: function (options) {
        return options && _.isString(options) ? options.split(',') : [];
      },
      initInputAttrs: function () {
        var value = this.attr('value');
        var options = this.attr('def.multi_choice_options');
        var type = this.attr('type');

        this.attr('input', {
          options: this.getOptions(options),
          value: mapValueFromCA(value, type),
          type: type,
          title: this.attr('def.title')
        });
      },
      updateValueInstance: function (value, type) {
        value = mapValuesToCA(value, type);
        this.attr('value', value || null);
        this.attr('isModified', this.attr('def.id'));
      },
      save: function (value) {
        var instance = this.attr('instance');
        var type = this.attr('type');

        this.attr('isSaving', true);

        this.updateValueInstance(value, type);
        instance.save()
          .done(function () {
            can.$(document.body).trigger('ajax:flash', {
              success: 'Saved'
            });
          })
          .fail(function () {
            can.$(document.body).trigger('ajax:flash', {
              error: 'There was a problem saving'
            });
          })
          .always(function () {
            this.attr('isSaving', false);
          }.bind(this));
      }
    },
    events: {
      init: function () {
        this.scope.initInputAttrs();
      },
      '{scope.input} value': function (scope, ev, val) {
        this.scope.save(val);
      }
    }
  });
})(window._, window.can, window.GGRC);
