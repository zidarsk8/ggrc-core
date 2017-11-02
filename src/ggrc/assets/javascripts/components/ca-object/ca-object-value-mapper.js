/*
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {
  convertFromCaValue,
  convertToCaValue,
} from '../../plugins/utils/ca-utils';

(function (_, can, GGRC) {
  'use strict';

  GGRC.Components('customAttributesObjectValueMapper', {
    tag: 'ca-object-value-mapper',
    template: '<content></content>',
    scope: {
      input: {
        value: null,
        type: null,
        options: [],
        placeholder: 'Please enter the value...',
      },
      value: null,
      valueObj: null,
      type: null,
      def: null,
      initInput: function () {
        this.attr('input', {
          options: this.getOptions(),
          value: this.getValue(),
          type: this.getType(),
          title: this.getTitle(),
        });
      },
      getOptions: function () {
        var options = this.attr('def.multi_choice_options');
        return options && _.isString(options) ? options.split(',') : [];
      },
      getTitle: function () {
        return this.attr('def.title');
      },
      getType: function () {
        var type = this.attr('type');
        return type;
      },
      getValue: function () {
        return convertFromCaValue(
          this.attr('type'),
          this.attr('value'),
          this.attr('valueObj')
        );
      },
      setValue: function (value) {
        this.attr('value',
          convertToCaValue(
            value,
            this.attr('type')
          )
        );
      },
    },
    events: {
      init: function () {
        this.scope.initInput();
      },
      '{scope.input} value': function (scope, ev, val) {
        this.scope.setValue(val);
      },
    },
  });
})(window._, window.can, window.GGRC);
