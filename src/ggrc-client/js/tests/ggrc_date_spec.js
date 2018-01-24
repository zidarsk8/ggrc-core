/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

'use strict';

describe('GGRC.Date module', function () {
  describe('getDate() method', function () {
    let method;

    beforeAll(function () {
      method = GGRC.Date.getDate;
    });

    it('returns date for Date object parameter', function () {
      let expected = new Date();
      let actual = method(expected);

      expect(actual).toEqual(expected);
    });

    it('returns null for null parameter', function () {
      let actual = method(null);

      expect(actual).toBeNull();
    });

    describe('when date format is not specified', function () {
      it('returns null for Date in moment display format', function () {
        let param = '04/30/2017';
        let actual = method(param);

        expect(actual).toBeNull();
      });

      it('returns null for Date in picker ISO format', function () {
        let param = '17-04-30';
        let actual = method(param);

        expect(actual).toBeNull();
      });

      it('returns null for Date in picker display format', function () {
        let param = '04/30/17';
        let actual = method(param);

        expect(actual).toBeNull();
      });

      it('returns correct Date for Date in moment ISO format', function () {
        let dateString = '2017-04-30';
        let expected = new Date(2017, 3, 30);
        let actual = method(dateString);

        expect(actual).toEqual(expected);
      });
    });

    it('returns null when date string is not in correct date format',
      function () {
        let dateString = '2017/04/30';
        let dateFormat = 'YYYY/DD/MM';
        let actual = method(dateString, dateFormat);

        expect(actual).toBeNull();
      });

    it('returns expected Date when date string is in correct date format',
      function () {
        let dateString = '2017/30/04';
        let dateFormat = 'YYYY/DD/MM';
        let expected = new Date(2017, 3, 30);
        let actual = method(dateString, dateFormat);

        expect(actual).toEqual(expected);
      });
  });
});
