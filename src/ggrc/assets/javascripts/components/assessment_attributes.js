/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  can.Component.extend({
    tag: 'assessment-template-attributes',
    template: '<content></content>',
    scope: {
      fields: new can.List()
    }
  });
  can.Component.extend({
    tag: 'template-filed',
    template: can.view(GGRC.mustache_path + '/assessment_templates/attribute_field.mustache'),
    scope: {
      removeField: function (scope, el, ev) {

      },
      attrs: function () {
        return _.compact(_.map(this.attr('field.values').split(','), function (value) {
          value = $.trim(value);
          if (value) {
            return value;
          }
        }));
      }
    }
  });
  can.Component.extend({
    tag: 'add-template-filed',
    template: can.view(GGRC.mustache_path + '/assessment_templates/attribute_add_field.mustache'),
    scope: {
      selected: new can.Map(),
      types: [{
        type: 'Dropdown',
        text: 'Type values separated by comma'
      }, {
        type: 'Checkbox',
        text: 'Type label'
      }, {
        type: 'Radio',
        text: 'Type values separated by comma'
      }, {
        type: 'Text',
        text: 'Type description'
      }],
      addFiled: function (scope, el, ev) {
        var fields = this.attr('fields');
        var selected = this.attr('selected');

        ev.preventDefault();

        fields.push({
          title: selected.title,
          type: selected.type,
          values: selected.values
        });
        _.each(['title', 'values'], function (type) {
          selected.attr(type, '');
        });
      }
    },
    events: {
      inserted: function () {
        if (!this.scope.attr('selected.type')) {
          this.scope.attr('selected', this.scope.attr('types')[0]);
        }
      }
    },
    helpers: {
      placeholder: function (options) {
        var types = this.attr('types');
        var item = _.findWhere(types, {
          type: this.attr('selected.type')
        });
        if (item) {
          return item.text;
        }
      }
    }
  });
})(window.can, window.can.$);
