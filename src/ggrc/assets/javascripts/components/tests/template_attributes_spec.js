/*!
  Copyright (C) 2016 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.templateAttributes', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('templateAttributes');
  });

  describe('fieldRemoved() method', function () {
    var method;  // the method under test
    var scope;

    beforeEach(function () {
      scope = new can.Map({
        fields: []
      });
      method = Component.prototype.scope.fieldRemoved.bind(scope);
    });

    it('removes the deleted field from the fields list', function () {
      var remainingFields;
      var $el = $('<p></p>');
      var eventObj = $.Event('on-delete');

      var deletedField = new can.Map({id: 4, title: 'bar'});

      var currentFields = [
        new can.Map({id: 17, title: 'foo'}),
        new can.Map({id: 4, title: 'bar'}),
        new can.Map({id: 52, title: 'baz'})
      ];
      scope.attr('fields').replace(currentFields);

      method(deletedField, $el, eventObj);

      remainingFields = _.map(scope.fields, 'title');
      expect(remainingFields).toEqual(['foo', 'baz']);
    });
  });
});
