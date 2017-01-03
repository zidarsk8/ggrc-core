/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Component.CommentInput', function () {
  'use strict';

  var testingText = 'Lorem ipsum ' +
    'dolor sit amet, consectetur adipiscing elit.' +
    ' Mauris accumsan porta nisl ut lobortis.' +
    ' Proin sollicitudin enim ante,' +
    ' sit amet elementum ipsum fringilla sed';

  var defaultText = 'Some text';

  describe('.setValues() method', function () {
    var Component;  // the component under test
    var setValues;
    var scope;

    beforeEach(function () {
      Component = GGRC.Components.get('commentInput');
      scope = new can.Map(Component.prototype.scope);
      // Set some default values before each test run to check values are updated
      scope.attr('value', defaultText);
      scope.attr('isEmpty', false);
      setValues = Component.prototype.scope.setValues.bind(scope);
    });

    it('should update: value and isEmpty. length is > 0 ', function () {
      setValues(testingText);

      expect(scope.attr('value')).toBe(testingText);
      expect(scope.attr('isEmpty')).toBe(false);
    });
    it('should update: value and isEmpty. length is equal 0 ', function () {
      setValues(null);

      expect(scope.attr('value')).toBe(null);
      expect(scope.attr('isEmpty')).toBe(true);
    });
    it('should update multiple times: value and isEmpty.', function () {
      setValues(null);

      expect(scope.attr('value')).toBe(null);
      expect(scope.attr('isEmpty')).toBe(true);

      setValues(testingText);

      expect(scope.attr('value')).toBe(testingText);
      expect(scope.attr('isEmpty')).toBe(false);

      setValues(null);

      expect(scope.attr('value')).toBe(null);
      expect(scope.attr('isEmpty')).toBe(true);
    });
  });
});
