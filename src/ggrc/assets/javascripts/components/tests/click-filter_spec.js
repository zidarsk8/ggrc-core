/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.clickFilter', function () {
  'use strict';

  describe('click action', function () {
    var method;
    var element;
    var event;
    var viewModel;
    var $element;
    var delay = 300;

    beforeEach(function () {
      var component;
      viewModel = new can.Map({
        delay: delay
      });
      element = {};
      $element = $(element);
      event = {
        stopPropagation: jasmine.createSpy('stopPropagation')
      };
      component = GGRC.Components.get('clickFilter');
      method = component.prototype.events.click.bind({
        viewModel: viewModel
      });

      jasmine.clock().install();
    });

    afterEach(function () {
      jasmine.clock().uninstall();
    });

    it('must disable the element', function () {
      var before = $element.prop('disabled');
      var after;

      method(element, event);
      after = $element.prop('disabled');

      expect(before).toBeFalsy();
      expect(after).toBeTruthy();
    });

    it('must enable the element after defined delay time', function () {
      var result;

      method(element, event);
      jasmine.clock().tick(delay + 1);
      result = $element.prop('disabled');

      expect(result).toBe(false);
    });

    it('must stop a propagation if element is disabled', function () {
      method(element, event); // first click
      method(element, event); // second click

      expect(event.stopPropagation).toHaveBeenCalledTimes(1);
    });
  });
});
