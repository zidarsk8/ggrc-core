/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: peter@reciprocitylabs.com
 Maintained By: peter@reciprocitylabs.com
 */

describe('GGRC.Components.addTemplateField', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('addTemplateField');
  });

  describe('addField() method', function () {
    var addField;  // the method under test
    var $el;
    var ev;
    var scope;

    beforeEach(function () {
      var parentScope = {
        attr: function (attrName) {
          return {};
        }
      };
      var scope_ = Component.prototype.scope({}, parentScope);
      addField = scope_.addField;

      $el = $('<div></div>');
      ev = {
        preventDefault: jasmine.createSpy()
      };
      scope = new can.Map({
        fields: new can.List(),
        selected: new can.Map(),
        valueAttrs: ['Dropdown'],
        id: 123
      });
    });
    it('does not require the "values" field to add a field of type Map:Person',
      function (done) {
        var selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Map:Person',
          values: ''
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
        var selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Dropdown',
          values: 'value0 value1'
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
        var selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Dropdown',
          values: ''
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
        var selectedObj = new can.Map({
          title: 'External Reviewer',
          type: 'Text',
          values: ''
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
        var selectedObj = new can.Map({
          title: '',
          type: 'Text',
          values: ''
        });
        scope.attr('selected', selectedObj);
        addField.call(scope, scope, $el, ev);
        setTimeout(function () {
          expect(scope.fields.length).toEqual(0);
          done();
        }, 3);
      }
    );
    it('requires the "type" field to add a field',
      function (done) {
        var selectedObj = new can.Map({
          title: 'Title example',
          type: '',
          values: ''
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
});
