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
        let values = _.splitTrim(selected.values, {
          unique: true,
        }).join(',');
        ev.preventDefault();
        viewModel.attr('selected.invalidValues', false);
        viewModel.attr('selected.invalidTitleError', '');

        let isInvalidTitle = this.isTitleInvalid(title, fields);
        let isInvalidValue = this
          .isInvalidValues(viewModel.valueAttrs, type, values);

        if (isInvalidTitle || isInvalidValue) {
          if (isInvalidValue) {
            viewModel.attr('selected.invalidValues', true);
          }

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
      isEqualTitle(title, attr) {
        return attr && attr.toLowerCase() === title.toLowerCase();
      },
      isReservedByCustomAttr(title) {
        const customAttrs = GGRC.custom_attr_defs
          .filter((attr) =>
            attr.definition_type && attr.definition_type === 'assessment'
          ).filter((attr) =>
            this.isEqualTitle(title, attr.title)
          );

        return customAttrs.length;
      },
      isTitleInvalid(title, fields) {
        if (this.isEmptyTitle(title)) {
          this.attr(
            'selected.invalidTitleError',
            'A custom attribute title can not be blank'
          );
          return true;
        }

        if (this.isDublicateTitle(fields, title)) {
          this.attr(
            'selected.invalidTitleError',
            'A custom attribute with this title already exists'
          );
          return true;
        }

        if (this.isReservedByCustomAttr(title)) {
          this.attr(
            'selected.invalidTitleError',
            'Custom attribute with such name already exists'
          );
          return true;
        }

        return false;
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
