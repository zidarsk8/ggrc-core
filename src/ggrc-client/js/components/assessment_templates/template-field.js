/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {
  ddValidationValueToMap,
  ddValidationMapToValue,
} from '../../plugins/utils/ca-utils';
import template from './templates/attribute_field.mustache';

/*
 * Template field
 *
 * Represents each `field` passed from assessment-template-attributes `fields`
 */
export default can.Component.extend({
  tag: 'template-field',
  template,
  scope: function (attrs, parentScope, element) {
    return {
      types: parentScope.attr('types'),

      _EV_FIELD_REMOVED: 'on-remove',

      /*
       * Removes `field` from `fields`
       */
      removeField: function (scope, el, ev) {
        ev.preventDefault();

        // CAUTION: In order for the event to not get lost, triggering it
        // must happen before changing any of the scope attributes that
        // cause changes in the template.
        this.$rootEl.triggerHandler({
          type: this._EV_FIELD_REMOVED,
        });

        scope.attr('_pending_delete', true);
      },
      /*
       * Denormalize field.multi_choice_mandatory into opts
       * "0, 1, 2" is normalized into
       * [
       * {value: 0, attachment: false, comment: false},
       * {value: 1, attachment: false, comment: true},
       * {value: 2, attachment: true, comment: false},
       * ]
       */
      denormalize_mandatory: function (field, flags) {
        let options = _.splitTrim(field.attr('multi_choice_options'));
        let vals = _.splitTrim(field.attr('multi_choice_mandatory'));
        let isEqualLength = options.length === vals.length;
        let range;

        if (!isEqualLength && options.length < vals.length) {
          vals.length = options.length;
        } else if (!isEqualLength && options.length > vals.length) {
          range = _.range(options.length - vals.length);
          range = range.map(function () {
            return '0';
          });
          vals = vals.concat(range);
        }

        return _.zip(options, vals).map(function (zip) {
          let attr = new can.Map();
          let val = parseInt(zip[1], 10);
          attr.attr('value', zip[0]);
          attr.attr(ddValidationValueToMap(val));
          return attr;
        });
      },
      /*
       * Normalize opts into field.multi_choice_mandatory
       * [
       * {value: 0, attachment: true, comment: false},
       * {value: 1, attachment: true, comment: true},
       * ]
       * is normalized into "2, 3" (10b, 11b).
       */
      normalize_mandatory: function (attrs) {
        return can.map(attrs, ddValidationMapToValue).join(',');
      },
    };
  },
  events: {
    /**
     * The component's entry point.
     *
     * @param {Object} element - the (unwrapped) DOM element that triggered
     *   creating the component instance
     * @param {Object} options - the component instantiation options
     */
    init: function (element, options) {
      const field = this.scope.attr('field');
      const denormalized = this.scope.denormalize_mandatory(field);
      const types = this.scope.attr('types');
      const item = _.find(types, function (obj) {
        return obj.type === field.attr('attribute_type');
      });
      this.scope.field.attr('attribute_name', item.name);
      this.scope.attr('attrs', denormalized);

      this.scope.attr('$rootEl', $(element));
    },
    '{attrs} change': function () {
      const attrs = this.scope.attr('attrs');
      const normalized = this.scope.normalize_mandatory(attrs);
      this.scope.field.attr('multi_choice_mandatory', normalized);
    },
  },
});
