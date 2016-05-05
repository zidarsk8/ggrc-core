/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe('CMS.Controllers.TreeViewNode', function () {
  'use strict';

  var Ctrl;  // the controller under test

  beforeAll(function () {
    Ctrl = CMS.Controllers.TreeViewNode;
  });

  describe('draw_node() method', function () {
    var ctrlInst;  // fake controller instance
    var ifNotRemovedResult;  // fake return value of the _ifNotRemoved() method
    var method;
    var $element;

    beforeEach(function () {
      ifNotRemovedResult = {};
      $element = $('<div></div>');

      ctrlInst = {
        options: new can.Map({
          show_view: '/foo/bar.mustache'
        }),
        element: $element,
        _draw_node_in_progress: false,
        _draw_node_deferred: new can.Deferred(),
        add_child_lists_to_child: jasmine.createSpy(),
        _ifNotRemoved: jasmine.createSpy().and.returnValue(ifNotRemovedResult),
        replace_element: jasmine.createSpy()
      };

      method = Ctrl.prototype.draw_node.bind(ctrlInst);

      spyOn(can, 'view');
    });

    it('renders the DOM element with the "active" CSS class if node active',
      function () {
        var callArgs;
        var callback;

        ctrlInst.options.attr('isActive', false);
        $element.addClass('active');

        method();

        expect(can.view).toHaveBeenCalledWith(
          '/foo/bar.mustache',
          ctrlInst.options,
          ifNotRemovedResult
        );

        expect(ctrlInst._ifNotRemoved).toHaveBeenCalled();
        callArgs = ctrlInst._ifNotRemoved.calls.mostRecent().args;
        callback = callArgs[0];

        // simulate invoking the callback and observe the effect
        $element.removeClass('active');
        callback();

        expect(ctrlInst.element.hasClass('active')).toBe(true);
      }
    );

    it('renders the DOM element without the "active" CSS class if ' +
      'node not active',
      function () {
        var callArgs;
        var callback;

        ctrlInst.options.attr('isActive', false);
        $element.removeClass('active');  // make sure it is indeed inactive

        method();

        expect(can.view).toHaveBeenCalledWith(
          '/foo/bar.mustache',
          ctrlInst.options,
          ifNotRemovedResult
        );

        expect(ctrlInst._ifNotRemoved).toHaveBeenCalled();
        callArgs = ctrlInst._ifNotRemoved.calls.mostRecent().args;
        callback = callArgs[0];

        // simulate invoking the callback and observe the effect
        callback();

        expect(ctrlInst.element.hasClass('active')).toBe(false);
      }
    );
  });
});
