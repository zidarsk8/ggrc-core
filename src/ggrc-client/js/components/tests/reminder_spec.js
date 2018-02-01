/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.reminder', function () {
  'use strict';

  let Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('reminder');
  });

  describe('reminder() method', function () {
    let eventObj;
    let instance;
    let method;  // the method under test
    let pendingRefresh;
    let pendingSave;
    let scope;
    let $element;

    beforeEach(function () {
      pendingRefresh = new can.Deferred();
      pendingSave = new can.Deferred();

      instance = new can.Map({
        refresh: jasmine.createSpy('refresh')
                        .and.returnValue(pendingRefresh.promise()),
        save: jasmine.createSpy('save')
                     .and.returnValue(pendingSave.promise()),
      });

      scope = new can.Map({
        instance: instance,
      });
      eventObj = $.Event();
      $element = $('<div></div>');

      method = Component.prototype.scope.reminder.bind(scope);
    });

    it('saves the instance only after it has been refreshed', function () {
      method(scope, $element, eventObj);

      expect(instance.save).not.toHaveBeenCalled();
      pendingRefresh.resolve(instance);
      expect(instance.save).toHaveBeenCalled();
    });
  });
});
