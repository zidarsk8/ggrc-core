/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.gDrivePickerLauncher', function () {
  'use strict';

  var Component;
  var events;
  var viewModel;
  var eventStub = {
    preventDefault: function () {}
  };

  beforeAll(function () {
    Component = GGRC.Components.get('gDrivePickerLauncher');
    events = Component.prototype.events;
  });

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('gDrivePickerLauncher');
  });

  describe('onClickHandler() method', function () {
    it('call confirmationCallback() if it is provided', function () {
      spyOn(viewModel, 'confirmationCallback');

      viewModel.onClickHandler(null, null, eventStub);

      expect(viewModel.confirmationCallback).toHaveBeenCalled();
    });

    it('pass callbackResult to can.when()', function () {
      var dfd = can.Deferred();
      var thenSpy = jasmine.createSpy('then');
      spyOn(viewModel, 'confirmationCallback').and.returnValue(dfd);
      spyOn(can, 'when').and.returnValue({
        then: thenSpy
      });

      viewModel.onClickHandler(null, null, eventStub);

      expect(can.when).toHaveBeenCalledWith(dfd);
      expect(thenSpy).toHaveBeenCalled();
    });

    it('pass null to can.when() when callback is not provided', function () {
      var thenSpy = jasmine.createSpy('then');
      spyOn(can, 'when').and.returnValue({
        then: thenSpy
      });

      viewModel.onClickHandler(null, null, eventStub);

      expect(can.when).toHaveBeenCalledWith(null);
      expect(thenSpy).toHaveBeenCalled();
    });
  });

  describe('onKeyup() method', function () {
    describe('if escape key was clicked', function () {
      let event;
      let element;

      beforeEach(function () {
        const ESCAPE_KEY_CODE = 27;
        event = {
          keyCode: ESCAPE_KEY_CODE,
          stopPropagation: jasmine.createSpy('stopPropagation'),
        };
        element = $('<div></div>');
      });

      it('calls stopPropagation for passed event', function () {
        viewModel.onKeyup(element, event);
        expect(event.stopPropagation).toHaveBeenCalled();
      });

      it('unsets focus for element', function (done) {
        const blur = function () {
          done();
          element.off('blur', blur);
        };
        element.on('blur', blur);
        viewModel.onKeyup(element, event);
      });
    });
  });

  describe('events', function () {
    describe('"{viewModel} modal:success" handler', function () {
      var method;
      var that;

      beforeEach(function () {
        that = {
          viewModel: viewModel
        };
        method = events['{viewModel} modal:success'].bind(that);
      });

      it('calls callback if callback is provided', function () {
        viewModel.attr('itemsUploadedCallback', jasmine.createSpy('callback'));
        method();
        expect(viewModel.itemsUploadedCallback).toHaveBeenCalled();
      });

      it('refreshes instance if callback is not provided', function () {
        viewModel.instance = jasmine.createSpyObj('instance',
          ['reify', 'refresh']);
        method();
        expect(viewModel.instance.reify).toHaveBeenCalled();
        expect(viewModel.instance.refresh).toHaveBeenCalled();
      });
    });
  });
});
