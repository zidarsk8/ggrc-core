/*!
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('can.Model.Mixin.isOverdue', function () {
  'use strict';

  var Mixin;

  beforeAll(function () {
    Mixin = CMS.Models.Mixins.isOverdue;
  });

  describe('_isOverdue() method: ', function () {
    var instance;
    var method;

    beforeEach(function () {
      instance = new can.Map({
        next_due_date: '2030-01-01',
        status: 'Not Started'
      });
      method = Mixin.prototype._isOverdue;
    });

    it('is defined', function () {
      expect(method).toBeDefined();
    });

    it('returns false, if status is "Verified" ' +
    'and is_verification_needed is true', function () {
      instance.attr('next_due_date', moment().subtract(1, 'd'));
      instance.attr('is_verification_needed', true);
      instance.attr('status', 'Verified');

      expect(method.apply(instance)).toEqual(false);
    });

    it('returns false, if status is "Finished"' +
    ' and is_verification_needed is false', function () {
      instance.attr('next_due_date', moment().subtract(1, 'd'));
      instance.attr('is_verification_needed', false);
      instance.attr('status', 'Finished');

      expect(method.apply(instance)).toEqual(false);
    });

    it('returns false, if status is not "Verified"' +
      ' and Next Due Date or End Date is later than today', function () {
      expect(method.apply(instance)).toEqual(false);
    });

    it('returns true, if status is not "Verified"' +
      ' and Next Due Date or' +
      ' End Date has already passed today\'s date', function () {
      instance.attr('next_due_date', '2015-01-01');
      expect(method.apply(instance)).toEqual(true);
    });

    it('returns true, if next_due_date is earlier than today', function () {
      var result;
      instance.attr('next_due_date', moment().subtract(1, 'd'));

      result = method.apply(instance);

      expect(result).toEqual(true);
    });

    it('returns false, if next_due_date is today', function () {
      var result;
      instance.attr('next_due_date', moment());

      result = method.apply(instance);

      expect(result).toEqual(false);
    });
  });
});
