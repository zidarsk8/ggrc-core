/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: andraz@reciprocitylabs.com
  Maintained By: andraz@reciprocitylabs.com
*/

describe('GGRC.Components.tabPanel', function () {
  'use strict';

  var instance;
  var scope;

  beforeAll(function () {
    instance = $(can.view.mustache('<tab-panel></tab-panel>')().children[0]);
    scope = instance.scope();
  });

  it('doesn\'t switch tabs when internal scope changes', function () {
    scope.attr("panels", new can.List([
      new can.Map(),
      new can.Map({
        panel: new can.Map()
      })
    ]));
    scope.attr("active", true);

    scope.attr("panels.0.foo", "bar");
    expect(scope.active).toEqual(true);

    scope.attr("panels.1.panel.active", true);
    expect(scope.active).toEqual(false);
  });
});
