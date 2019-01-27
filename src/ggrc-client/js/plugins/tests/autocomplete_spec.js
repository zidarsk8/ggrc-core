/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('ggrc.autocomplete widget', function () {
  'use strict';

  let context;
  let method;

  beforeEach(function () {
    context = {};
    method = $.cms_autocomplete.bind(context);
  });

  describe('cms_autocomplete() method', function () {
    it('gracefully handles a non-existing context element ', function () {
      context.element = null;
      try {
        method(undefined);
      } catch (err) {
        fail('An error left uncaught: ' + err.message);
      }
    });
  });
});
