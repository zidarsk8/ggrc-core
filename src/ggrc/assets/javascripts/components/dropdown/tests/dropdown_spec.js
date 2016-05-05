/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: peter@reciprocitylabs.com
 Maintained By: peter@reciprocitylabs.com
 */

describe('GGRC.Components.dropdown', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('dropdown');
  });

  describe('defining default scope values', function () {
    var scope;

    beforeAll(function () {
      scope = Component.prototype.scope;
    });

    it('sets the disable flag to false', function () {
      expect(scope.isDisabled).toBe(false);
    });
  });

  describe('init() method', function () {
    var componentInst;  // fake component instance
    var element;  // the DOM element passed to the component instance
    var init;  // the method under test
    var options;

    beforeEach(function () {
      element = $('<div></div>')[0];
      options = {};
      componentInst = {};
      componentInst.scope = new can.Map();
      init = Component.prototype.init.bind(componentInst);
    });

    it('sets the disable flag to false if the element\'s disable attribute ' +
        'is empty',
        function () {
          $(element).attr('is-disabled', '');
          componentInst.scope.attr('disable', true);
          init(element, options);
          expect(componentInst.scope.isDisabled).toBe(false);
        }
    );

    it('sets the disable flag to false if the element\'s disable attribute ' +
        'has a value false',
        function () {
          $(element).attr('is-disabled', 'false');
          componentInst.scope.attr('isDisabled', true);
          init(element, options);
          expect(componentInst.scope.attr('isDisabled')).toBe(false);
        }
    );

    it('sets the disable flag to true if the element\'s disable attribute ' +
        'has a value true',
        function () {
          $(element).attr('is-disabled', 'true');
          componentInst.scope.attr('isDisabled', false);
          init(element, options);
          expect(componentInst.scope.attr('isDisabled')).toBe(true);
        }
    );

    it('leaves the disable flag unchanged if the element\'s disable ' +
        'attribute is neither empty nor true/false',
        function () {
          $(element).attr('is-disabled', 'whatever');
          componentInst.scope.attr('isDisabled', true);
          init(element, options);
          expect(componentInst.scope.attr('isDisabled')).toBe(true);
        }
    );
  });
});
