

/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {modalAutocomplete} from '../autocomplete';

describe('autocomplete functionality', function () {
  describe('cms_autocomplete() method', function () {
    let context;

    beforeEach(function () {
      context = {};
    });

    it('gracefully handles a non-existing context element ', function () {
      context.element = null;
      try {
        modalAutocomplete();
      } catch (err) {
        fail('An error left uncaught: ' + err.message);
      }
    });
  });
});
