/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

'use strict';

describe('GGRC.Date module', function () {
  describe('getDate() method', function () {
    var method;

    beforeAll(function () {
      method = GGRC.Date.getDate;
    });

    it('returns date for Date object parameter', function () {
      var expected = new Date();
      var actual = method(expected);

      expect(actual).toEqual(expected);
    });

    it('returns null for null parameter', function () {
      var actual = method(null);

      expect(actual).toBeNull();
    });

    describe('when date format is not specified', function () {
      it('returns null for Date in moment display format', function () {
        var param = '04/30/2017';
        var actual = method(param);

        expect(actual).toBeNull();
      });

      it('returns null for Date in picker ISO format', function () {
        var param = '17-04-30';
        var actual = method(param);

        expect(actual).toBeNull();
      });

      it('returns null for Date in picker display format', function () {
        var param = '04/30/17';
        var actual = method(param);

        expect(actual).toBeNull();
      });

      it('returns correct Date for Date in moment ISO format', function () {
        var dateString = '2017-04-30';
        var expected = new Date(2017, 3, 30);
        var actual = method(dateString);

        expect(actual).toEqual(expected);
      });
    });

    it('returns null when date string is not in correct date format',
      function () {
        var dateString = '2017/04/30';
        var dateFormat = 'YYYY/DD/MM';
        var actual = method(dateString, dateFormat);

        expect(actual).toBeNull();
      });

    it('returns expected Date when date string is in correct date format',
      function () {
        var dateString = '2017/30/04';
        var dateFormat = 'YYYY/DD/MM';
        var expected = new Date(2017, 3, 30);
        var actual = method(dateString, dateFormat);

        expect(actual).toEqual(expected);
      });
  });
});
