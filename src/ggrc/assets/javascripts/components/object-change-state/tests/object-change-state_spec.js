/* !
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../object-change-state';

describe('GGRC.Components.objectChangeState', function () {
  var viewModel;

  beforeEach(function () {
    viewModel = new Component.prototype.viewModel;
  });

  describe('viewModel scope', function () {
    describe('changeState() method', function () {
      it('dipatches onStateChange event with passed status', function () {
        var newState = 'newState';

        spyOn(viewModel, 'dispatch');
        viewModel.changeState(newState);

        expect(viewModel.dispatch).toHaveBeenCalledWith({
          type: 'onStateChange',
          state: newState,
        });
      });
    });
  });

  describe('event scope', function () {
    var events;

    beforeEach(function () {
      events = Component.prototype.events;
    });

    describe('click handler', function () {
      var handler;
      var fakeEvent;

      beforeEach(function () {
        var eventScope = {
          viewModel: viewModel,
        };
        fakeEvent = new Event('click');
        handler = events.click.bind(eventScope);
      });

      it('changes state to viewModel.toState value with help a viewModel ' +
      'changeState method', function () {
        var toState = 'toState';
        spyOn(viewModel, 'changeState');
        viewModel.attr('toState', toState);
        handler({}, fakeEvent);
        expect(viewModel.changeState).toHaveBeenCalledWith(toState);
      });

      it('prevents default behavior for passed event', function () {
        spyOn(fakeEvent, 'preventDefault');
        handler({}, fakeEvent);
        expect(fakeEvent.preventDefault).toHaveBeenCalled();
      });
    });
  });
});
