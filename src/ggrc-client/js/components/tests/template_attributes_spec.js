/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.templateAttributes', function () {
  'use strict';

  let Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('templateAttributes');
  });

  describe('fieldRemoved() method', function () {
    let method;  // the method under test
    let scope;
    let remainingFields;
    let $el;
    let eventObj;

    beforeEach(function () {
      scope = new can.Map({
        fields: []
      });
      method = Component.prototype.scope.fieldRemoved.bind(scope);
      $el = $('<p></p>');
      eventObj = $.Event('on-delete');
    });

    it('removes the deleted field from the fields list', function () {
      let deletedField = new can.Map({id: 4, title: 'bar'});

      let currentFields = [
        new can.Map({id: 17, title: 'foo'}),
        new can.Map({id: 4, title: 'bar'}),
        new can.Map({id: 52, title: 'baz'})
      ];
      scope.attr('fields').replace(currentFields);

      method(deletedField, $el, eventObj);

      remainingFields = _.map(scope.fields, 'title');
      expect(remainingFields).toEqual(['foo', 'baz']);
    });

    it('removes the field without id from the fields list', function () {
      let deletedField = new can.Map({title: 'bar'});

      let currentFields = [
        new can.Map({id: 17, title: 'foo'}),
        new can.Map({title: 'bar'}),
        new can.Map({id: 52, title: 'baz'})
      ];
      scope.attr('fields').replace(currentFields);

      method(deletedField, $el, eventObj);

      remainingFields = _.map(scope.fields, 'title');
      expect(remainingFields).toEqual(['foo', 'baz']);
    });

    it('doesn\'t change the fields list if field doesn\'t match', function () {
      let deletedField = new can.Map({title: 'barbaz'});

      let currentFields = [
        new can.Map({id: 17, title: 'foo'}),
        new can.Map({id: 4, title: 'bar'}),
        new can.Map({id: 52, title: 'baz'})
      ];
      scope.attr('fields').replace(currentFields);

      spyOn(console, 'warn');

      method(deletedField, $el, eventObj);

      remainingFields = _.map(scope.fields, 'title');
      expect(remainingFields).toEqual(['foo', 'bar', 'baz']);
      expect(console.warn).toHaveBeenCalled();
    });
  });
});
