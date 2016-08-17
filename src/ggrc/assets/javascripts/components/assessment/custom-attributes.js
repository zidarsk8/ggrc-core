/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';
  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/custom-attributes.mustache');

  GGRC.Components('assessmentCustomAttributes', {
    tag: 'assessment-custom-attributes',
    template: tpl,
    scope: {
      instance: null,
      needConfirm: false,
      values: null,
      definitions: null,
      isModified: null,
      modal: {
        open: false
      },
      items: [],
      prepareCustomAttributeValues: function (defs, values) {
        var scope = this;
        return can.map(defs, function (def) {
          var valueData = false;
          var id = def.id;
          var type = GGRC.Utils.mapCAType(def.attribute_type);
          var stub = {
            attributable_id: scope.id,
            custom_attribute_id: id,
            attribute_value: null,
            preconditions_failed: (def.mandatory) ? ['value'] : [],
            def: def,
            attributeType: type
          };

          can.each(values, function (value) {
            if (value.custom_attribute_id === id) {
              value.attr('def', def);
              value.attr('attributeType', type);
              //value.attr('id', value.id);
              value.attribute_value = value.attribute_object ?
                value.attribute_object.reify() : value.attribute_value;
              valueData = value;
            }
          });

          return valueData || new can.Map(stub);
        });
      },
      refresh: function () {
        var scope = this;
        scope.attr('values')
          .replace(scope.prepareCustomAttributeValues(scope.attr('definitions'),
            scope.attr('values')));
        scope.attr('items', scope.attr('values'));
      }
    },
    init: function () {
      var scope = this.scope;
      var status = scope.instance.status;
      var needConfirm = status === 'Completed' || status === 'Verified';

      if (!scope.instance.class.is_custom_attributable) {
        return;
      }
      scope.attr('needConfirm', needConfirm);
    },
    events: {
      '{scope.instance} isReadyForRender': function (sc, ev, isReady) {
        var scope = this.scope;
        if (isReady) {
          scope.refresh();
        }
      }
    },
    helpers: {}
  });
})(window.can, window.GGRC, window.CMS);
