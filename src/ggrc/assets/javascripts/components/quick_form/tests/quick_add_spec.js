/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import ModalsController from '../../../controllers/modals_controller';

describe('GGRC.Components.quickAdd', function () {
  'use strict';
  var Component;
  var events;
  var scope;

  beforeAll(function () {
    Component = GGRC.Components.get('quickAdd');
    events = Component.prototype.events;
  });

  describe('"a[data-toggle=submit]:not(.disabled):not([disabled])' +
  ' click" event', function () {
    var handler;
    var element;
    var expectedParam = {
      modal_description: 'newDescription',
      modal_confirm: 'button',
      modal_title: 'title',
      button_view: '/static/mustache/quick_form/confirm_buttons.mustache'
    };
    var verifyDfd;

    beforeEach(function () {
      handler =
        events['a[data-toggle=submit]:not(.disabled):not([disabled]) click'];
      scope = new can.Map({
        modal_description: 'oldDescription',
        verify_event: false,
        modal_title: 'title',
        modal_button: 'button'
      });
      element = {
        context: {
          attributes: {
            modal_description: {value: 'newDescription'},
            verify_event: true
          }
        }
      };
      verifyDfd = can.Deferred();
      spyOn(can, 'Deferred')
        .and.returnValue(verifyDfd);
      spyOn(verifyDfd, 'resolve');
    });

    it('calls confirm panel if verify_event is true', function () {
      spyOn(ModalsController, 'confirm');
      handler.call({
        viewModel: scope,
        element: element
      });
      expect(ModalsController.confirm)
        .toHaveBeenCalledWith(expectedParam,
          verifyDfd.resolve, verifyDfd.reject);
    });
    it('does not call confirm panel if verify_event is false', function () {
      spyOn(ModalsController, 'confirm');
      element.context.attributes.verify_event = false;
      handler.call({
        viewModel: scope,
        element: element
      });
      expect(ModalsController.confirm)
        .not.toHaveBeenCalled();
    });
    it('sets scope.disabled to false after closing confirm panel',
      function () {
        spyOn(ModalsController, 'confirm')
          .and.returnValue(verifyDfd.reject());
        handler.call({
          viewModel: scope,
          element: element
        });
        expect(scope.attr('disabled')).toEqual(false);
      });
  });
});
