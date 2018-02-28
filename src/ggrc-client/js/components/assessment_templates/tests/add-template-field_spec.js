/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../add-template-field';

describe('add-template-field component', () => {
  describe('addField() method', () => {
    let addField; // the method under test
    let $el;
    let ev;
    let viewModel;
    let parentScope;
    let originalAttrDefs;
    let originalModelDefs;

    beforeAll(() => {
      originalAttrDefs = GGRC.custom_attr_defs;
      originalModelDefs = GGRC.model_attr_defs;
      GGRC.custom_attr_defs = [];
      GGRC.model_attr_defs = {
        Assessment: [],
      };
    });

    afterAll(() => {
      GGRC.custom_attr_defs = originalAttrDefs;
      GGRC.model_attr_defs = originalModelDefs;
    });

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
    });

    it('does not require the "values" field to add a field of type Map:Person',
      (done) => {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Map:Person',
          values: '',
        });
        viewModel.attr('selected', selectedObj);
        addField(viewModel, $el, ev);

        // FIXME: Because `addField` function calls `_.defer` we need to wait
        // for viewModel field to get updated.
        // It's necessary workaround because otherwise can.Map.validate function
        // prevents us adding new field. By using _.defer we wait for validate
        // function to get executed and only then we are adding
        setTimeout(() => {
          expect(viewModel.fields.length).toEqual(1);
          done();
        }, 3);
      }
    );
    it('requires the "values" field to add a field of type Dropdown',
      (done) => {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Dropdown',
          values: 'value0 value1',
        });
        viewModel.attr('selected', selectedObj);
        addField.call(viewModel, viewModel, $el, ev);
        setTimeout(function () {
          expect(viewModel.fields.length).toEqual(1);
          done();
        }, 3);
      }
    );
    it('requires the "values" field to add a field of type Dropdown',
      (done) => {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Dropdown',
          values: '',
        });
        viewModel.attr('selected', selectedObj);
        addField(viewModel, $el, ev);
        setTimeout(() => {
          expect(viewModel.fields.length).toEqual(0);
          done();
        }, 3);
      }
    );
    it('requires the "values" field to add a field of type Text',
      (done) => {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Text',
          values: '',
        });
        viewModel.attr('selected', selectedObj);
        addField(viewModel, $el, ev);
        setTimeout(() => {
          expect(viewModel.fields.length).toEqual(1);
          done();
        }, 3);
      }
    );
    it('requires the "title" field to add a field',
      (done) => {
        let selectedObj = new can.Map({
          title: '',
          type: 'Text',
          values: '',
        });
        viewModel.attr('selected', selectedObj);
        addField(viewModel, $el, ev);
        setTimeout(() => {
          expect(viewModel.fields.length).toEqual(0);
          done();
        }, 3);
      }
    );
  });

  describe('isEmptyTitle() method', () => {
    let isEmptyTitle; // the method under test
    let result;
    let selectedTitle;

    beforeAll(() => {
      let parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      let viewModel_ = Component.prototype.viewModel({}, parentScope);
      isEmptyTitle = viewModel_.isEmptyTitle;
    });

    beforeEach(() => {
      result = undefined;
    });

    it('has not to allow to input empty titles',
      (done) => {
        selectedTitle = '';

        result = isEmptyTitle(selectedTitle);

        expect(result).toEqual(true);
        done();
      }
    );
  });

  describe('isDublicateTitle() method', () => {
    let isDublicateTitle; // the method under test
    let result;
    let selectedTitle;
    let fields;

    beforeAll(() => {
      let parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      let viewModel_ = Component.prototype.viewModel({}, parentScope);
      isDublicateTitle = viewModel_.isDublicateTitle;
    });

    beforeEach(() => {
      fields = new can.List();
      result = undefined;
    });

    it('has to not allow to input titles that are already in "fields"',
      (done) => {
        fields.push({
          id: 123,
          title: 'title',
          attribute_type: 'Text',
          multi_choice_options: '',
          opts: new can.Map(),
        });
        selectedTitle = 'title';

        result = isDublicateTitle(fields, selectedTitle);

        expect(result).toEqual(true);
        done();
      }
    );

    it('has to allow to input titles that are not in "fields"',
      (done) => {
        fields.push({
          id: 123,
          title: 'title',
          attribute_type: 'Text',
          multi_choice_options: '',
          opts: new can.Map(),
        });
        selectedTitle = 'new title';

        result = isDublicateTitle(fields, selectedTitle);

        expect(result).toEqual(false);
        done();
      }
    );
  });

  describe('isInvalidValues() method', () => {
    let isInvalidValues; // the method under test
    let valueAttrs;
    let result;
    let parentScope;
    let viewModel_;

    beforeAll(() => {
      valueAttrs = ['Dropdown'];
      parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      viewModel_ = Component.prototype.viewModel({}, parentScope);
      isInvalidValues = viewModel_.isInvalidValues;
    });

    beforeEach(() => {
      result = undefined;
    });

    it('has to not allow to input type "Dropdown" with not set values',
      (done) => {
        result = isInvalidValues(valueAttrs, 'Dropdown', '');
        expect(result).toEqual(true);
        done();
      }
    );

    it('has to allow to input type "Dropdown" with set values',
      (done) => {
        result = isInvalidValues(valueAttrs, 'DropDown', 'some values');
        expect(result).toEqual(false);
        done();
      }
    );

    it('has to allow to input type "Text" with not set values',
      (done) => {
        result = isInvalidValues(valueAttrs, 'Text', '');
        expect(result).toEqual(false);
        done();
      }
    );
  });

  describe('isTitleInvalid() method', () => {
    let viewModel;
    let isTitleInvalid;

    beforeAll(() => {
      const parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      viewModel = Component.prototype.viewModel({}, parentScope);
      isTitleInvalid = viewModel.isTitleInvalid.bind(viewModel);
    });

    beforeEach(() => {
      viewModel.attr('selected.invalidTitleError', '');
    });

    function setupIsEmptyTitle() {
      spyOn(viewModel, 'isEmptyTitle').and
        .callFake((title) => !title);
    }

    function setupIsDublicateTitle() {
      spyOn(viewModel, 'isDublicateTitle').and
        .callFake((fields, title) => _.contains(fields, title));
    }

    it('should return false. correct value', () => {
      setupIsEmptyTitle();
      setupIsDublicateTitle();
      spyOn(viewModel, 'isReservedByCustomAttr').and.returnValue(false);
      spyOn(viewModel, 'isReservedByModelAttr').and.returnValue(false);

      const result = isTitleInvalid('my title', []);
      expect(result).toBeFalsy();
      expect(viewModel.attr('selected.invalidTitleError')).toEqual('');
      expect(viewModel.isEmptyTitle).toHaveBeenCalled();
      expect(viewModel.isDublicateTitle).toHaveBeenCalled();
      expect(viewModel.isReservedByCustomAttr).toHaveBeenCalled();
      expect(viewModel.isReservedByModelAttr).toHaveBeenCalled();
    });

    it('should return true. empty value', () => {
      setupIsEmptyTitle();
      setupIsDublicateTitle();
      const result = isTitleInvalid('', []);

      expect(result).toBeTruthy();
      expect(viewModel.attr('selected.invalidTitleError'))
        .toEqual('A custom attribute title can not be blank');
      expect(viewModel.isEmptyTitle).toHaveBeenCalled();
      expect(viewModel.isDublicateTitle).not.toHaveBeenCalled();
    });

    it('should return true. duplicated value', () => {
      setupIsEmptyTitle();
      setupIsDublicateTitle();
      const result = isTitleInvalid('my title', ['my title']);

      expect(result).toBeTruthy();
      expect(viewModel.attr('selected.invalidTitleError'))
        .toEqual('A custom attribute with this title already exists');
      expect(viewModel.isEmptyTitle).toHaveBeenCalled();
      expect(viewModel.isDublicateTitle).toHaveBeenCalled();
    });

    it('should return true. name reserved by custom att', () => {
      setupIsEmptyTitle();
      setupIsDublicateTitle();
      spyOn(viewModel, 'isReservedByCustomAttr').and.returnValue(true);
      const result = isTitleInvalid('new_checkbox');

      expect(result).toBeTruthy();
      expect(viewModel.attr('selected.invalidTitleError'))
        .toEqual('Custom attribute with such name already exists');
      expect(viewModel.isEmptyTitle).toHaveBeenCalled();
      expect(viewModel.isDublicateTitle).toHaveBeenCalled();
      expect(viewModel.isReservedByCustomAttr).toHaveBeenCalled();
    });

    it('should return true. name reserved by model att', () => {
      setupIsEmptyTitle();
      setupIsDublicateTitle();
      spyOn(viewModel, 'isReservedByCustomAttr').and.returnValue(false);
      spyOn(viewModel, 'isReservedByModelAttr').and.returnValue(true);
      const result = isTitleInvalid('code');

      expect(result).toBeTruthy();
      expect(viewModel.attr('selected.invalidTitleError'))
        .toEqual('Attribute with such name already exists');
      expect(viewModel.isEmptyTitle).toHaveBeenCalled();
      expect(viewModel.isDublicateTitle).toHaveBeenCalled();
      expect(viewModel.isReservedByCustomAttr).toHaveBeenCalled();
      expect(viewModel.isReservedByModelAttr).toHaveBeenCalled();
    });
  });

  describe('isReservedByCustomAttr() method', () => {
    let originalAttrDefs;
    let viewModel;
    let method;

    beforeAll(() => {
      originalAttrDefs = GGRC.custom_attr_defs;
      GGRC.custom_attr_defs = [
        {
          definition_type: 'assessment',
          title: 'New Checkbox',
        },
      ];
    });

    afterAll(() => {
      GGRC.custom_attr_defs = originalAttrDefs;
    });

    beforeEach(() => {
      const parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      viewModel = Component.prototype.viewModel({}, parentScope);
      method = viewModel.isReservedByCustomAttr.bind(viewModel);
    });

    it('should return false. Title is not reserved', () => {
      const result = method('my title');
      expect(result).toBeFalsy();
    });

    it('should return true. Reserved by custom attribute', () => {
      const result = method('new checkbox');
      expect(result).toBeTruthy();
    });
  });

  describe('isReservedByModelAttr() method', () => {
    let originalModelDefs;
    let viewModel;
    let method;

    beforeAll(() => {
      originalModelDefs = GGRC.model_attr_defs;
      GGRC.model_attr_defs = {
        Assessment: [
          {display_name: 'Code'},
        ],
      };
    });

    afterAll(() => {
      GGRC.model_attr_defs = originalModelDefs;
    });

    beforeEach(() => {
      const parentScope = new can.Map({
        attr: {},
        fields: [],
      });
      viewModel = Component.prototype.viewModel({}, parentScope);
      method = viewModel.isReservedByModelAttr.bind(viewModel);
    });

    it('should return false. Title is not reserved', () => {
      const result = method('my title');
      expect(result).toBeFalsy();
    });

    it('should return true. Reserved by model attribute', () => {
      const result = method('code');
      expect(result).toBeTruthy();
    });
  });
});
