/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  /*
   * Assessment template main component
   *
   * It collects fields data and it transforms them into appropriate
   * format for saving
   */
  can.Component.extend({
    tag: 'assessment-template-attributes',
    template: '<content></content>',
    scope: {
      fields: new can.List()
    }
  });

  /*
   * Template field
   *
   * Represents each `field` passed from assessment-template-attributes `fields`
   */
  can.Component.extend({
    tag: 'template-filed',
    template: can.view(GGRC.mustache_path +
      '/assessment_templates/attribute_field.mustache'),
    scope: {
      /*
       * Removes `field` from `fileds`
       */
      removeField: function (scope, el, ev) {
        ev.preventDefault();
        scope.attr('_pending_delete', true);
      },
      /*
       * Split field values
       *
       * @return {Array} attrs - Returns split values as an array
       */
      attrs: function () {
        if (_.contains(['Person', 'Text'], this.field.attr('type'))) {
          return [this.attr('field.multi_choice_options')];
        }
        return _.splitTrim(this.attr('field.multi_choice_options'), {
          compact: true
        });
      }
    }
  });
  can.Component.extend({
    tag: 'add-template-filed',
    template: can.view(GGRC.mustache_path +
      '/assessment_templates/attribute_add_field.mustache'),
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
      }, {
        type: 'Person',
        text: 'Type description'
      }],
      valueAttrs: ['Dropdown', 'Checkbox', 'Radio'],
      /*
       * Create new field
       *
       * Field must contain value title, type, values and opts.
       * Opts are populated, once we start changing checkbox values
       *
       * @param {Object} scope - current (add-template-field) scope
       * @param {jQuery.Object} el - clicked element
       * @param {Object} ev - click event handler
       */
      addField: function (scope, el, ev) {
        var fields = this.attr('fields');
        var selected = this.attr('selected');
        var title = _.trim(selected.title);
        var type = _.trim(selected.type);
        var values = _.splitTrim(selected.values, {
          unique: true
        }).join(',');

        ev.preventDefault();
        if (!type || !title ||
            (_.contains(scope.valueAttrs, type) && !values)) {
          return;
        }

        fields.push({
          title: title,
          attribute_type: type,
          multi_choice_options: values,
          opts: new can.Map()
        });
        _.each(['title', 'multi_choice_options'], function (type) {
          selected.attr(type, '');
        });
      }
    },
    events: {
      /*
       * Set default dropdown type on init
       */
      inserted: function () {
        var types = this.scope.attr('types');

        if (!this.scope.attr('selected.type')) {
          this.scope.attr('selected.type', _.first(types).attr('type'));
        }
      }
    },
    helpers: {
      /*
       * Get input placeholder value depended on type
       *
       * @param {Object} options - Mustache options
       */
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
