/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('can.mustache.helper.normalizeLink', () => {
  let helper;

  beforeEach(() => {
    helper = can.Mustache._helpers.normalizeLink.fn;
  });

  describe('normalizeUrl(url) method', () => {
    it('should not throw error when url is falsy', () => {
      [null, undefined, ''].forEach((link) => {
        expect(() => helper(link)).not.toThrowError();
      });
    });

    it('should not change links with http/https protocol and related', () => {
      ['http://google.com',
        'https://google.com',
        'ftp://127.0.0.1:80',
        '/controls/10'].forEach((link) => {
        let result = helper(link);

        expect(result).toBe(link);
      });
    });

    it('should add http protocol to the link', () => {
      ['www.google.com',
        'google.com',
        'any text'].forEach((link) => {
        let result = helper(link);

        expect(result).toBe(`http://${link}`);
      });
    });
  });
});
