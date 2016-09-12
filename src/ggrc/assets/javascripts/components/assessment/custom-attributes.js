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
      values: null,
      definitions: null,
      isModified: null,
      modal: {
        open: false
      },
      items: [],
      updateValues: function (defs, values) {
        var scope = this;
        return can.map(defs, function (def) {
          var valueData = false;
          var id = def.id;
          var type = GGRC.Utils.mapCAType(def.attribute_type);
          var stub = {
            isStub: true,
            attributable_id: scope.id,
            custom_attribute_id: id,
            attribute_value: null,
            attribute_object: null,
            preconditions_failed: (def.mandatory) ? ['value'] : [],
            def: def,
            attributeType: type
          };

          can.each(values, function (value) {
            if (value.custom_attribute_id === id) {
              value.attr('def', def);
              value.attr('attributeType', type);
              value.attr('preconditions_failed',
                value.attr('preconditions_failed') || []);
              valueData = value;
            }
          });

          return valueData || new can.Map(stub);
        });
      },
      refresh: function (isReady) {
        var scope = this;
        if (isReady) {
          scope.attr('values')
            .replace(scope.updateValues(scope.attr('definitions'),
              scope.attr('values')));
          scope.attr('items', scope.attr('values'));
        }
      }
    },
    init: function () {
      var isReady = this.scope.attr('instance.isReadyForRender');
      this.scope.refresh(isReady);
    },
    events: {
      '{scope.instance} isReadyForRender': function (sc, ev, isReady) {
        this.scope.refresh(isReady);
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
