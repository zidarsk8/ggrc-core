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

        let validators = this.getValidators(title, fields);
        this.validateTitle(validators);
        this.validateValues(viewModel, type, values);

        if (
          viewModel.attr('selected.invalidValues') ||
          viewModel.attr('selected.invalidTitleError')
        ) {
          return;
        }

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
      },
      validateValues(viewModel, type, values) {
        let invalidValues = _.includes(viewModel.valueAttrs, type) && !values;
        viewModel.attr('selected.invalidValues', invalidValues);
      },
      validateTitle(validators) {
        const errorMessage = validators.reduce((prev, next) => {
          if (prev) {
            return prev;
          }

          return next();
        }, '');

        this.attr('selected.invalidTitleError', errorMessage);
      },
      getValidators(title, fields) {
        return [
          isEmptyTitle.bind(null, title),
          isDublicateTitle.bind(null, fields, title),
          isReservedByCustomAttr.bind(null, title),
          isReservedByModelAttr.bind(null, title),
        ];
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

const isEqualTitle = (title, attr) => {
  return attr && attr.toLowerCase() === title.toLowerCase();
};

const isDublicateTitle = (fields, selectedTitle) => {
  let duplicateField = _.some(fields, (item) => {
    return item.title.toLowerCase() === selectedTitle.toLowerCase() &&
      !item._pending_delete;
  });
  return fields.length && duplicateField ?
    'A custom attribute with this title already exists' :
    '';
};

const isEmptyTitle = (selectedTitle) => {
  return !selectedTitle ?
    'A custom attribute title can not be blank' :
    '';
};

const isReservedByCustomAttr = (title) => {
  const customAttrs = GGRC.custom_attr_defs
    .filter((attr) =>
      attr.definition_type && attr.definition_type === 'assessment'
    ).filter((attr) =>
      isEqualTitle(title, attr.title)
    );

  return customAttrs.length ?
    'Custom attribute with such name already exists' :
    '';
};

const isReservedByModelAttr = (title) => {
  const modelAttrs = GGRC.model_attr_defs.Assessment.filter(
    (attr) => isEqualTitle(title, attr.display_name)
  );

  return modelAttrs.length ?
    'Attribute with such name already exists' :
    '';
};

export {
  isDublicateTitle,
  isEmptyTitle,
  isReservedByCustomAttr,
  isReservedByModelAttr,
};
