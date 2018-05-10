/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.UnarchiveLink', function () {
  'use strict';

  let Component;

  beforeAll(function () {
    Component = GGRC.Components.get('unarchiveLink');
  });

  describe('click() event', function () {
    let displayName = 'DISPLAY NAME';
    let notifyText = 'was unarchived successfully';
    let eventObj;
    let instance;
    let pendingSave;
    let scope;
    let $element;
    let event;

    beforeEach(function () {
      pendingSave = new can.Deferred();

      instance = new can.Map({
        save: jasmine.createSpy('save')
          .and.returnValue(pendingSave.promise()),
        display_name: function () {
          return displayName;
        },
      });

      scope = new can.Map({
        instance: instance,
        notifyText: notifyText,
      });
      eventObj = $.Event();
      $element = $('<div></div>');

      spyOn($.fn, 'trigger').and.callThrough();

      event = Component.prototype.events['a click']
        .bind({scope: scope});
    });

    it('instance was not unarchived if was not archived', function () {
      event($element, eventObj);

      expect(instance.attr('archived')).toBeFalsy();
      expect(instance.save).not.toHaveBeenCalled();
      expect($.fn.trigger).not.toHaveBeenCalled();
    });

    it('instance was saved without notification', function () {
      instance.attr('archived', true);

      event($element, eventObj);
      pendingSave.resolve();

      expect(instance.attr('archived')).toBeFalsy();
      expect(instance.save).toHaveBeenCalled();
      expect($.fn.trigger).not.toHaveBeenCalled();
    });

    it('instance was saved without notification', function () {
      let successMessage = displayName + ' ' + notifyText;
      instance.attr('archived', true);
      scope.attr('notify', true);

      event($element, eventObj);
      pendingSave.resolve();

      expect(instance.attr('archived')).toBeFalsy();
      expect(instance.save).toHaveBeenCalled();
      expect($.fn.trigger).toHaveBeenCalledWith('ajax:flash',
        {success: [successMessage]});
    });
  });
});
