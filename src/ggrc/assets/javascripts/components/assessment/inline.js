/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/inline/inline.mustache');
  var innerTplFolder = GGRC.mustache_path + '/components/assessment/inline';

  function getTemplateByType(type) {
    type = can.Mustache.resolve(type);
    return innerTplFolder + '/' + type + '.mustache';
  }

  GGRC.Components('assessmentInlineEdit', {
    tag: 'assessment-inline-edit',
    template: tpl,
    scope: {
      titleText: null,
      type: null,
      value: null,
      options: null,
      readonly: false, // whether or not the value can be edited
      isSaving: false,
      isEdit: false,
      context: {
        value: null,
        options: null
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
       */
      enableEdit: function (scope) {
        if (scope.attr('readonly')) {
          return;
        }
        if (scope.needConfirm) {
          scope.confirmEdit.confirm(scope.instance,
            scope.confirmEdit).done(function () {
              scope.attr('isEdit', true);
            });
        } else {
          scope.attr('isEdit', true);
        }
      },
      onCancel: function (scope) {
        scope.attr('isEdit', false);
        scope.attr('context.value', scope.attr('_value'));
      },
      onSave: function () {
        var oldValue = this.attr('value');
        var value = this.attr('context.value');

        this.attr('isEdit', false);

        if (oldValue === value) {
          return;
        }
        this.attr('_value', oldValue);
        this.attr('value', value);
        this.attr('isSaving', true);
      }
    },
    init: function () {
      var scope = this.scope;
      var value = scope.attr('value');

      scope.attr('_value', value);
      scope.attr('context.value', value);
    },
    events: {
      '{window} mousedown': function (el, ev) {
        var scope = this.scope;
        var isInside = this.element.has(ev.target).length ||
          this.element.is(ev.target);

        if (!isInside && scope.attr('isEdit')) {
          _.defer(function () {
            scope.onSave();
          });
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
