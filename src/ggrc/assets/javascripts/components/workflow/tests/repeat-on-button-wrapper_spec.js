/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.repeatOnButtonWrapper', function () {
  'use strict';

  var viewModel;

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('repeatOnButtonWrapper');
  });

  describe('setRepeatOn method', function () {
    it('should set unit and repeat_every properties', function () {
      var unit = 'Day';
      var repeatEvery = '2';

      viewModel.setRepeatOn(unit, repeatEvery);

      expect(viewModel.attr('instance.unit'))
        .toEqual(unit);
      expect(viewModel.attr('instance.repeat_every'))
        .toEqual(repeatEvery);
    });
  });

  describe('updateRepeatOn method', function () {
    var saveDfd;
    var instance;

    beforeEach(function () {
      instance = viewModel.attr('instance');
      saveDfd = can.Deferred();
      instance.save = jasmine.createSpy('save')
        .and
        .returnValue(saveDfd);
      spyOn($.prototype, 'trigger');
    });

    it('should notify when update was successful', function () {
      viewModel.updateRepeatOn();
      saveDfd.resolve();

      expect(instance.save.calls.count()).toEqual(1);
      expect($.prototype.trigger)
        .toHaveBeenCalledWith(
          'ajax:flash',
          {success: 'Repeat updated successfully'});
    });

    it('should notify when update was unsuccessful', function () {
      viewModel.updateRepeatOn();
      saveDfd.reject();

      expect(instance.save.calls.count()).toEqual(1);
      expect($.prototype.trigger)
        .toHaveBeenCalledWith(
          'ajax:flash',
          {error: 'An error occurred'});
    });
  });

  describe('onSetRepeat method', function () {
    var saveDfd;
    var instance;
    beforeEach(function () {
      instance = viewModel.attr('instance');
      saveDfd = can.Deferred();
      instance.save = jasmine.createSpy('save')
        .and
        .returnValue(saveDfd);
      spyOn($.prototype, 'trigger');
    });

    it('should update instance values when auto-save disabled',
    function () {
      var unit = 'Week';
      var repeatEvery = '22';
      viewModel.onSetRepeat(unit, repeatEvery);
      expect(instance.save.calls.count()).toEqual(0);
      expect(viewModel.attr('instance.unit'))
        .toEqual(unit);
      expect(viewModel.attr('instance.repeat_every'))
        .toEqual(repeatEvery);
    });

    it('should save instance when auto-save enabled',
    function () {
      var unit = 'Week';
      var repeatEvery = '22';
      viewModel.attr('autoSave', true);
      viewModel.onSetRepeat(unit, repeatEvery);
      saveDfd.resolve();
      expect(viewModel.attr('instance.unit'))
        .toEqual(unit);
      expect(viewModel.attr('instance.repeat_every'))
        .toEqual(repeatEvery);
      expect(instance.save.calls.count()).toEqual(1);
    });
  });
});
