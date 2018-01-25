/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.addTemplateField', function () {
  'use strict';

  let Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('addTemplateField');
  });

  describe('addField() method', function () {
    let addField;  // the method under test
    let $el;
    let ev;
    let scope;
    let parentScope;
    let scope_;

    beforeEach(function () {
      parentScope = {
        attr: function () {
          return {};
        },
      };
      scope_ = Component.prototype.scope({}, parentScope);
      addField = scope_.addField;

      $el = $('<div></div>');
      ev = {
        preventDefault: jasmine.createSpy(),
      };
      scope = new can.Map({
        fields: new can.List(),
        selected: new can.Map(),
        valueAttrs: ['Dropdown'],
        id: 123,
        isDublicateTitle: scope_.isDublicateTitle.bind(scope),
        isEmptyTitle: scope_.isEmptyTitle.bind(scope),
        isInvalidValues: scope_.isInvalidValues.bind(scope),
      });
    });

    it('does not require the "values" field to add a field of type Map:Person',
      function (done) {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Map:Person',
          values: '',
        });
        scope.attr('selected', selectedObj);
        addField.call(scope, scope, $el, ev);

        // FIXME: Because `addField` function calls `_.defer` we need to wait
        // for scope field to get updated.
        // It's necessary workaround because otherwise can.Map.validate function
        // prevents us adding new field. By using _.defer we wait for validate
        // function to get executed and only then we are adding
        setTimeout(function () {
          expect(scope.fields.length).toEqual(1);
          done();
        }, 3);
      }
    );
    it('requires the "values" field to add a field of type Dropdown',
      function (done) {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Dropdown',
          values: 'value0 value1',
        });
        scope.attr('selected', selectedObj);
        addField.call(scope, scope, $el, ev);
        setTimeout(function () {
          expect(scope.fields.length).toEqual(1);
          done();
        }, 3);
      }
    );
    it('requires the "values" field to add a field of type Dropdown',
      function (done) {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Dropdown',
          values: '',
        });
        scope.attr('selected', selectedObj);
        addField.call(scope, scope, $el, ev);
        setTimeout(function () {
          expect(scope.fields.length).toEqual(0);
          done();
        }, 3);
      }
    );
    it('requires the "values" field to add a field of type Text',
      function (done) {
        let selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Text',
          values: '',
        });
        scope.attr('selected', selectedObj);
        addField.call(scope, scope, $el, ev);
        setTimeout(function () {
          expect(scope.fields.length).toEqual(1);
          done();
        }, 3);
      }
    );
    it('requires the "title" field to add a field',
      function (done) {
        let selectedObj = new can.Map({
          title: '',
          type: 'Text',
          values: '',
        });
        scope.attr('selected', selectedObj);
        addField.call(scope, scope, $el, ev);
        setTimeout(function () {
          expect(scope.fields.length).toEqual(0);
          done();
        }, 3);
      }
    );
  });

  describe('isEmptyTitle() method', function () {
    let isEmptyTitle;  // the method under test
    let result;
    let selectedTitle;

    beforeAll(function () {
      let parentScope = {
        attr: function () {
          return {};
        },
      };
      let scope_ = Component.prototype.scope({}, parentScope);
      isEmptyTitle = scope_.isEmptyTitle;
    });

    beforeEach(function () {
      result = undefined;
    });

    it('has not to allow to input empty titles',
      function (done) {
        selectedTitle = '';

        result = isEmptyTitle(selectedTitle);

        expect(result).toEqual(true);
        done();
      }
    );
  });

  describe('isDublicateTitle() method', function () {
    let isDublicateTitle;  // the method under test
    let result;
    let selectedTitle;
    let fields;

    beforeAll(function () {
      let parentScope = {
        attr: function () {
          return {};
        },
      };
      let scope_ = Component.prototype.scope({}, parentScope);
      isDublicateTitle = scope_.isDublicateTitle;
    });

    beforeEach(function () {
      fields = new can.List();
      result = undefined;
    });

    it('has to not allow to input titles that are already in "fields"',
      function (done) {
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
      function (done) {
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

  describe('isInvalidValues() method', function () {
    let isInvalidValues;  // the method under test
    let valueAttrs;
    let result;
    let parentScope;
    let scope_;

    beforeAll(function () {
      valueAttrs = ['Dropdown'];
      parentScope = {
        attr: function () {
          return {};
        },
      };
      scope_ = Component.prototype.scope({}, parentScope);
      isInvalidValues = scope_.isInvalidValues;
    });

    beforeEach(function () {
      result = undefined;
    });

    it('has to not allow to input type "Dropdown" with not set values',
      function (done) {
        result = isInvalidValues(valueAttrs, 'Dropdown', '');
        expect(result).toEqual(true);
        done();
      }
    );

    it('has to allow to input type "Dropdown" with set values',
      function (done) {
        result = isInvalidValues(valueAttrs, 'DropDown', 'some values');
        expect(result).toEqual(false);
        done();
      }
    );

    it('has to allow to input type "Text" with not set values',
      function (done) {
        result = isInvalidValues(valueAttrs, 'Text', '');
        expect(result).toEqual(false);
        done();
      }
    );
  });
});
