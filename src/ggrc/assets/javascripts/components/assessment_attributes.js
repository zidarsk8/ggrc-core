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
        var fileds = scope.attr('fields');
        var field = scope.attr('field');
        var index = _.findIndex(fileds, function (item) {
          return item.type === field.type && item.title === field.title;
        });

        ev.preventDefault();
        if (index !== -1) {
          fileds.splice(index, 1);
        }
      },
      attrs: function () {
        return _.splitTrim(this.attr('field.values'), {
          compact: true
        });
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
      addField: function (scope, el, ev) {
        var fields = this.attr('fields');
        var selected = this.attr('selected');
        var title = _.trim(selected.title);
        var type = _.trim(selected.type);
        var values = _.splitTrim(selected.values, {
          unique: true
        }).join(',');

        ev.preventDefault();
        if (!type || !values || !title) {
          return;
        }

        fields.push({
          title: title,
          type: type,
          values: values,
          opts: new can.Map()
        });
        _.each(['title', 'values'], function (type) {
          selected.attr(type, '');
        });
      }
    },
    events: {
      inserted: function () {
        var types = this.scope.attr('types');

        if (!this.scope.attr('selected.type')) {
          this.scope.attr('selected.type', _.first(types).attr('type'));
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
