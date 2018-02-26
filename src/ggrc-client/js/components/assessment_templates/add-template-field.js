/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './templates/add-template-field.mustache';

export default can.Component.extend({
  tag: 'add-template-field',
  template,
  viewModel(attrs, parentScope) {
    return new can.Map({
      selected: new can.Map(),
      fields: parentScope.attr('fields'),
      types: parentScope.attr('types'),
      // the field types that require a list of possible values to be defined
      valueAttrs: ['Dropdown'],
      /*
       * Create a new field.
       *
       * Field must contain value title, type, values.
       * Opts are populated, once we start changing checkbox values
       *
       * @param {can.Map} viewModel - the current (add-template-field) viewModel
       * @param {jQuery.Object} el - the clicked DOM element
       * @param {Object} ev - the event object
       */
      addField(viewModel, el, ev) {
        let fields = viewModel.attr('fields');
        let selected = viewModel.attr('selected');
        let title = _.trim(selected.title);
        let type = _.trim(selected.type);
        let invalidInput = false;
        let values = _.splitTrim(selected.values, {
          unique: true,
        }).join(',');
        ev.preventDefault();
        viewModel.attr('selected.invalidTitle', false);
        viewModel.attr('selected.emptyTitle', false);
        viewModel.attr('selected.dublicateTitle', false);
        viewModel.attr('selected.invalidValues', false);

        if (this.isEmptyTitle(title)) {
          this.attr('selected.invalidTitle', true);
          this.attr('selected.emptyTitle', true);
          invalidInput = true;
        } else if (this.isDublicateTitle(fields, title)) {
          this.attr('selected.invalidTitle', true);
          this.attr('selected.dublicateTitle', true);
          invalidInput = true;
        }
        if (this.isInvalidValues(viewModel.valueAttrs, type, values)) {
          viewModel.attr('selected.invalidValues', true);
          invalidInput = true;
        }
        if (invalidInput) {
          return;
        }
        // We need to defer adding in modal since validation is preventing
        // on adding the first item
        _.defer(() => {
          fields.push({
            id: viewModel.attr('id'),
            title: title,
            attribute_type: type,
            multi_choice_options: values,
          });
          _.each(['title', 'values', 'multi_choice_options'],
            (type) => {
              selected.attr(type, '');
            });
        });
      },
      isInvalidValues(valueAttrs, type, values) {
        return _.contains(valueAttrs, type) && !values;
      },
      isDublicateTitle(fields, selectedTitle) {
        let duplicateField = _.some(fields, (item) => {
          return item.title === selectedTitle && !item._pending_delete;
        });
        return fields.length && duplicateField;
      },
      isEmptyTitle(selectedTitle) {
        return !selectedTitle;
      },
    });
  },
  events: {
    /*
     * Set default dropdown type on init
     */
    init() {
      let types = this.viewModel.attr('types');
      if (!this.viewModel.attr('selected.type')) {
        this.viewModel.attr('selected.type', _.first(types).attr('type'));
      }
    },
  },
  helpers: {
    /*
     * Get input placeholder value depended on type
     *
     * @param {Object} options - Mustache options
     */
    placeholder(options) {
      let types = this.attr('types');
      let item = _.findWhere(types, {
        type: this.attr('selected.type'),
      });
      if (item) {
        return item.text;
      }
    },
  },
});
