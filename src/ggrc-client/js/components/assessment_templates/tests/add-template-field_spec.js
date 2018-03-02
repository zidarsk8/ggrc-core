/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component, * as Validations from '../add-template-field';

describe('add-template-field component', () => {
  describe('addField() method', () => {
    let addField; // the method under test
    let $el;
    let ev;
    let viewModel;
    let parentScope;

    beforeEach(() => {
      parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      viewModel = Component.prototype.viewModel({}, parentScope);
      addField = viewModel.addField.bind(viewModel);

      $el = $('<div></div>');
      ev = {
        preventDefault: jasmine.createSpy(),
      };

      spyOn(viewModel, 'getValidators').and.returnValue([]);
    });

    it('does not require the "values" field to add a field of type Map:Person',
      () => {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Map:Person',
          values: '',
        });
        viewModel.attr('selected', selectedObj);
        addField(viewModel, $el, ev);
        expect(viewModel.fields.length).toEqual(1);
      }
    );
    it('requires the "values" field to add a field of type Dropdown', () => {
      let selectedObj = new can.Map({
        title: 'External Reviewer',
        type: 'Dropdown',
        values: 'value0 value1',
      });
      viewModel.attr('selected', selectedObj);
      addField.call(viewModel, viewModel, $el, ev);
      expect(viewModel.fields.length).toEqual(1);
    });
    it('requires the "values" field to add a field of type Dropdown', () => {
      let selectedObj = new can.Map({
        title: 'External Reviewer',
        type: 'Dropdown',
        values: '',
      });
      viewModel.attr('selected', selectedObj);
      addField(viewModel, $el, ev);
      expect(viewModel.fields.length).toEqual(0);
    });
    it('requires the "values" field to add a field of type Text', () => {
      let selectedObj = new can.Map({
        title: 'External Reviewer',
        type: 'Text',
        values: '',
      });
      viewModel.attr('selected', selectedObj);
      addField(viewModel, $el, ev);
      expect(viewModel.fields.length).toEqual(1);
    });
  });

  describe('isEmptyTitle() method', () => {
    let isEmptyTitle; // the method under test

    beforeAll(() => {
      isEmptyTitle = Validations.isEmptyTitle;
    });

    it('should return error message', () => {
      let selectedTitle = '';
      let result = isEmptyTitle(selectedTitle);

      expect(result).toEqual('A custom attribute title can not be blank');
    });

    it('should not return error message', () => {
      let selectedTitle = 'my title';
      let result = isEmptyTitle(selectedTitle);

      expect(result).toEqual('');
    });
  });

  describe('isDublicateTitle() method', () => {
    let isDublicateTitle; // the method under test

    beforeAll(() => {
      isDublicateTitle = Validations.isDublicateTitle;
    });

    it('should return error message', () => {
      const fields = [{
        id: 123,
        title: 'TiTlE',
        attribute_type: 'Text',
        multi_choice_options: '',
      }];
      const selectedTitle = 'title';

      expect(isDublicateTitle(fields, selectedTitle))
        .toEqual('A custom attribute with this title already exists');
    });

    it('should not return error message', () => {
      const fields = [{
        id: 123,
        title: 'title',
        attribute_type: 'Text',
        multi_choice_options: '',
      }];
      const selectedTitle = 'new title';

      expect(isDublicateTitle(fields, selectedTitle)).toEqual('');
    });
  });

  describe('isReservedByCustomAttr() method', () => {
    let originalAttrDefs;
    let method;

    beforeAll(() => {
      originalAttrDefs = GGRC.custom_attr_defs;
      GGRC.custom_attr_defs = [
        {
          definition_type: 'assessment',
          title: 'New Checkbox',
        },
      ];

      method = Validations.isReservedByCustomAttr;
    });

    afterAll(() => {
      GGRC.custom_attr_defs = originalAttrDefs;
    });

    it('should not return error message', () => {
      expect(method('my title')).toEqual('');
    });

    it('should return error message', () => {
      expect(method('new checkbox'))
        .toEqual('Custom attribute with such name already exists');
    });
  });

  describe('isReservedByModelAttr() method', () => {
    let originalModelDefs;
    let method;

    beforeAll(() => {
      originalModelDefs = GGRC.model_attr_defs;
      GGRC.model_attr_defs = {
        Assessment: [
          {display_name: 'Code'},
        ],
      };

      method = Validations.isReservedByModelAttr;
    });

    afterAll(() => {
      GGRC.model_attr_defs = originalModelDefs;
    });

    it('should not return error message', () => {
      expect(method('my title')).toEqual('');
    });

    it('should return error message', () => {
      expect(method('code'))
        .toEqual('Attribute with such name already exists');
    });
  });

  describe('validateValues() method', () => {
    let validateValues; // the method under test
    let viewModel;

    beforeEach(() => {
      const parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      viewModel = Component.prototype.viewModel({}, parentScope);
      validateValues = viewModel.validateValues;
    });

    it('has to not allow to input type "Dropdown" with not set values', () => {
      validateValues(viewModel, 'Dropdown', '');
      expect(viewModel.attr('selected.invalidValues')).toBeTruthy();
    });

    it('has to allow to input type "Dropdown" with set values', () => {
      validateValues(viewModel, 'DropDown', 'some values');
      expect(viewModel.attr('selected.invalidValues')).toBeFalsy();
    });

    it('has to allow to input type "Text" with not set values', () => {
      validateValues(viewModel, 'Text', '');
      expect(viewModel.attr('selected.invalidValues')).toBeFalsy();
    });
  });

  describe('validateTitle() method', () => {
    let viewModel;
    let validateTitle;

    beforeAll(() => {
      const parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      viewModel = Component.prototype.viewModel({}, parentScope);
      validateTitle = viewModel.validateTitle.bind(viewModel);
    });

    beforeEach(() => {
      viewModel.attr('selected.invalidTitleError', '');
    });

    function getTitleError() {
      return viewModel.attr('selected.invalidTitleError');
    }

    function setupSpies(caErrorMsg, modelAttrErrorMsg) {
      spyOn(Validations, 'isEmptyTitle').and
        .callFake((title) => !title ? 'empty val message' : '');

      spyOn(Validations, 'isDublicateTitle').and
        .callFake((fields, title) => {
          return _.contains(fields, title) ?
            'duplicates val message' :
            '';
        });

      spyOn(Validations, 'isReservedByCustomAttr')
        .and.returnValue(caErrorMsg);
      spyOn(Validations, 'isReservedByModelAttr')
        .and.returnValue(modelAttrErrorMsg);

      spyOn(viewModel, 'getValidators').and
        .callFake((title, fields) => {
          return [
            Validations.isEmptyTitle.bind(null, title),
            Validations.isDublicateTitle.bind(null, fields, title),
            Validations.isReservedByCustomAttr.bind(null, title),
            Validations.isReservedByModelAttr.bind(null, title),
          ];
        });
    }

    it('should not set error message', () => {
      setupSpies('', '');

      let validators = viewModel.getValidators('my title', []);
      validateTitle(validators);

      expect(getTitleError()).toEqual('');
      expect(Validations.isEmptyTitle).toHaveBeenCalled();
      expect(Validations.isDublicateTitle).toHaveBeenCalled();
      expect(Validations.isReservedByCustomAttr).toHaveBeenCalled();
      expect(Validations.isReservedByModelAttr).toHaveBeenCalled();
    });

    it('should set "empty value" error message', () => {
      setupSpies('', '');

      let validators = viewModel.getValidators('', []);
      validateTitle(validators);

      expect(getTitleError()).toEqual('empty val message');
      expect(Validations.isEmptyTitle).toHaveBeenCalled();
      expect(Validations.isDublicateTitle).not.toHaveBeenCalled();
      expect(Validations.isReservedByCustomAttr).not.toHaveBeenCalled();
      expect(Validations.isReservedByModelAttr).not.toHaveBeenCalled();
    });

    it('should set "duplicated value" error message', () => {
      setupSpies('', '');

      let validators = viewModel.getValidators('my title', ['my title']);
      validateTitle(validators);

      expect(getTitleError()).toEqual('duplicates val message');
      expect(Validations.isEmptyTitle).toHaveBeenCalled();
      expect(Validations.isDublicateTitle).toHaveBeenCalled();
      expect(Validations.isReservedByCustomAttr).not.toHaveBeenCalled();
      expect(Validations.isReservedByModelAttr).not.toHaveBeenCalled();
    });

    it('should set "custom attr" error message', () => {
      const expectedMessage = 'custom attr message';
      setupSpies(expectedMessage, '');

      let validators = viewModel.getValidators('new_checkbox', []);
      validateTitle(validators);

      expect(getTitleError()).toEqual(expectedMessage);
      expect(Validations.isEmptyTitle).toHaveBeenCalled();
      expect(Validations.isDublicateTitle).toHaveBeenCalled();
      expect(Validations.isReservedByCustomAttr).toHaveBeenCalled();
      expect(Validations.isReservedByModelAttr).not.toHaveBeenCalled();
    });

    it('should set "model attr" error message', () => {
      const expectedMessage = 'model attr message';
      setupSpies('', expectedMessage);

      let validators = viewModel.getValidators('code', []);
      validateTitle(validators);

      expect(getTitleError()).toEqual(expectedMessage);
      expect(Validations.isEmptyTitle).toHaveBeenCalled();
      expect(Validations.isDublicateTitle).toHaveBeenCalled();
      expect(Validations.isReservedByCustomAttr).toHaveBeenCalled();
      expect(Validations.isReservedByModelAttr).toHaveBeenCalled();
    });
  });
});
