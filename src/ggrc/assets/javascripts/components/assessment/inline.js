/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/inline/inline.mustache');
  var innerTplFolder = GGRC.mustache_path + '/components/assessment/inline';

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

  function getTemplateByType(type) {
    type = can.Mustache.resolve(type);
    return innerTplFolder + '/' + type + '.mustache';
  }

  GGRC.Components('assessmentInlineEdit', {
    tag: 'assessment-inline-edit',
    template: tpl,
    scope: {
      instance: null,
      titleText: null,
      type: '@',
      caId: null,
      property: '@',
      value: null,
      valueId: null,
      values: null,
      valuesValidation: null,
      readonly: false, // whether or not the value can be edited
      isSaving: false,
      emptyText: '@',
      $rootEl: null,
      context: {
        isEdit: false,
        value: null,
        values: null
      },
      getRequiredAttachments: function () {
        var FLAGS = {
          COMMENT: 1,
          ATTACHMENT: 2
        };
        var attr = this.attr();
        var values = attr.values || '';
        var valuesValidation = attr.valuesValidation || '';
        var value = attr.context.value;
        var requiredFields = [];
        var i;
        var mandatory;

        if (!values || !value) {
          return requiredFields;
        }
        i = values.split(',').indexOf(value);
        mandatory = valuesValidation.split(',')[i];

        if (mandatory === undefined) {
          return requiredFields;
        }

        mandatory = parseInt(mandatory, 10);

        if (mandatory & FLAGS.COMMENT) {
          requiredFields.push('comment');
        }

        if (mandatory & FLAGS.ATTACHMENT) {
          requiredFields.push('evidence');
        }
        return requiredFields;
      },
      addComment: function () {
        this.addAttachment(false);
      },
      addAttachment: function (fields) {
        can.batch.start();
        this.attr('instance._modifiedAttribute', {
          fieldTitleText: this.attr('titleText'),
          value: this.attr('context.value'),
          caId: this.attr('caId'),
          valueId: this.attr('valueId'),
          type: this.attr('type'),
          modalTitleText: fields && fields.length ?
            'Required ' + fields.map(function (field) {
              return can.capitalize(field);
            }).join(' and ') : 'Add comment',
          requiredAttachments: fields && fields.length ? fields : ['comment']
        });
        can.batch.stop();

        this.attr('instance._modifiedAttribute.showModal', true);
      },
      setPerson: function (scope, el, ev) {
        this.attr('context.value', ev.selectedItem.serialize());
      },
      unsetPerson: function (scope, el, ev) {
        ev.preventDefault();
        this.attr('context.value', undefined);
      },

      /**
       * Enter the edit mode if editing is allowed (i.e. the readonly option is
       * not set). If the readonly option is enabled, do not do anything.
       *
       * @param {can.Map} scope - the scope object itself (this)
       * @param {jQuery.Element} $el - the DOM element that triggered the event
       * @param {jQuery.Event} ev - the event object
       */
      enableEdit: function (scope, $el, ev) {
        ev.preventDefault();

        if (!this.attr('readonly')) {
          if (scope.needConfirm) {
            scope.confirmEdit.confirm(scope.instance,
              scope.confirmEdit).done(function () {
                this.attr('context.isEdit', true);
              }.bind(this));
          } else {
            this.attr('context.isEdit', true);
          }
        }
      },
      onCancel: function (ctx, el, ev) {
        ev.preventDefault();
        this.attr('context.isEdit', false);
        this.attr('context.value', this.attr('_value'));
      },
      onSave: function (ctx, el, ev) {
        var property = this.attr('property');
        var instance = this.attr('instance');
        var oldValue = this.attr('value');
        var value = this.attr('context.value');
        var type = this.attr('type');

        ev.preventDefault();

        this.attr('context.isEdit', false);

        if (oldValue === value) {
          return;
        }

        this.attr('_value', oldValue);
        this.attr('isSaving', true);

        instance.refresh().then(function () {
          if (this.attr('caId')) {
            value = mapValuesToCA(value, type);

            instance.attr('custom_attributes.' + this.attr('caId'), value);
          } else {
            instance.attr(property, value);
          }

          instance.save().done(function () {
            $(document.body).trigger('ajax:flash', {
              success: 'Saved'
            });
            this.afterSave();
          }.bind(this)).fail(function (instance, err) {
            this.attr('context.value', this.attr('_value'));
            GGRC.Errors.notifier('error')(err);
          }.bind(this)).always(function () {
            this.attr('isSaving', false);
          }.bind(this));
        }.bind(this));
      },
      afterSave: function afterSave() {
        var requiredAttachments = this.getRequiredAttachments();
        if (requiredAttachments.length) {
          this.addAttachment(requiredAttachments);
        }
      }
    },
    init: function init(el, options) {
      var scope = this.scope;
      var value = scope.attr('value');
      var values = scope.attr('values');
      var property = scope.attr('property');
      var instance = scope.attr('instance');
      var type = scope.attr('type');

      scope.attr('$rootEl', el);

      if (scope.attr('caId')) {
        value = mapValueForCA(value, type);

        if (!scope.attr('emptyText')) {
          scope.attr('emptyText', 'None'); // default for custom attributes
        }
      }

      if (property) {
        value = instance.attr(property);
      }
      scope.attr('_value', value);
      scope.attr('context.value', value);

      if (values && _.isString(values)) {
        values = values.split(',');
      }

      scope.attr('context.values', values);
    },

    events: {
      '{window} mousedown': function (el, ev) {
        var scope = this.scope;
        var isInside = this.element.has(ev.target).length ||
          this.element.is(ev.target);

        if (!isInside && scope.attr('context.isEdit')) {
          _.defer(function () {
            scope.onSave(scope, this.element, ev);
          }.bind(this));
        }
      }
    },
    helpers: {
      renderInnerTemplateByType: function (type, options) {
        return can.view.render(getTemplateByType(type), options.context);
      }
    }
  });
})(window._, window.can, window.GGRC);
