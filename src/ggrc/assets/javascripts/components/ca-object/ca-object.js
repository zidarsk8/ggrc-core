/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/ca-object/ca-object.mustache');

  function mapValueForCA(value, type) {
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
      return value ? 'Person:' + value.id : value;
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
      type: null,
      def: null,
      value: null,
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
      updateValueInstance: function (value) {
        this.attr('value', value || null);
        this.attr('isModified', this.attr('def').id);
      },
      save: function (value) {
        var instance = this.attr('instance');
        var type = this.attr('type');
        value = mapValuesToCA(value, type);
        this.updateValueInstance(value);
        instance.save()
          .done(function () {
            $(document.body).trigger('ajax:flash', {
              success: 'Saved'
            });
          })
          .fail(function () {
            $(document.body).trigger('ajax:flash', {
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
        var scope = this.scope;
        var value = scope.attr('value');
        var options = scope.attr('def.multi_choice_options');
        var type = scope.attr('type');

        if (options && _.isString(options)) {
          options = options.split(',');
        }

        this.scope.attr('input', {
          options: options,
          value: mapValueForCA(value, type),
          type: type,
          title: scope.attr('def.title')
        });
        console.info('This scope', this.scope.attr());
      },
      '{scope.input} value': function (scope, ev, val) {
        this.scope.save(val);
      }
    }
  });
})(window._, window.can, window.GGRC);
