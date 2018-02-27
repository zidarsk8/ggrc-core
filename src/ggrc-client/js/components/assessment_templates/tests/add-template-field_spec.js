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
});
