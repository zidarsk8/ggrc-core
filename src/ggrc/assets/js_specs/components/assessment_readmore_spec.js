/*!
  Copyright (C) 2016 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Component.Assessment.ReadMore', function () {
  'use strict';

  var readMore = 'Read More';
  var testText = 'Test text';
  var btnNewText = 'Read Less';

  var defaultScopeState = {
    text: null,
    isExpanded: false,
    showButton: false,
    btnText: readMore,
    maxHeight: '108px'
  };

  describe('.restoreDefaults() method', function () {
    var Component;  // the component under test
    var restoreDefault;
    var scope;

    beforeEach(function () {
      Component = GGRC.Components.get('assessmentReadMore');
      scope = new can.Map(Component.prototype.scope);
      restoreDefault = Component.prototype.scope.restoreDefault;
      restoreDefault = restoreDefault.bind(scope);
    });

    it('restores default scope', function () {
      scope.attr('text', testText);
      scope.attr('isExpanded', true);
      scope.attr('showButton', true);
      scope.attr('btnText', btnNewText);

      restoreDefault();

      expect(scope.attr('text')).toBe(testText);
      expect(scope.attr('isExpanded')).toBe(defaultScopeState.isExpanded);
      expect(scope.attr('showButton')).toBe(defaultScopeState.showButton);
      expect(scope.attr('btnText')).toBe(defaultScopeState.btnText);
    });
  });

  describe('.toggle() method', function () {
    var Component;  // the component under test
    var toggle;
    var scope;

    beforeEach(function () {
      Component = GGRC.Components.get('assessmentReadMore');
      scope = new can.Map(Component.prototype.scope);
      toggle = Component.prototype.scope.toggle;
      toggle = toggle.bind(scope);
    });

    it('switch default state', function () {
      scope.attr('isExpanded', true);
      scope.attr('btnText', btnNewText);
      scope.attr('maxHeight', '100%');

      toggle();

      expect(scope.attr('maxHeight')).toBe(defaultScopeState.maxHeight);
      expect(scope.attr('isExpanded')).toBe(defaultScopeState.isExpanded);
      expect(scope.attr('btnText')).toBe(defaultScopeState.btnText);
    });
  });
});
