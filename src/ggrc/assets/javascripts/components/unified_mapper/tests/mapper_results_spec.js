/*!
  Copyright (C) 2016 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.mapperResults', function () {
  'use strict';

  describe('on inserted event', function () {
    var scope;
    var $body;
    var $root;  // the component's root DOM element

    beforeEach(function () {
      var renderer = can.view.mustache('<mapper-results></mapper-results>');

      $body = $('body');
      $body.append(renderer());
      $root = $body.find('mapper-results');

      scope = $root.scope();
    });

    afterEach(function () {
      $root.remove();
    });

    it('initializes the list of entries to an empty list', function () {
      expect(scope.entries).toBeDefined();
      expect(scope.entries.attr()).toEqual([]);
    });

    it('initializes the options to an empty list', function () {
      expect(scope.options).toBeDefined();
      expect(scope.options.attr()).toEqual([]);
    });
  });
});
