/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe('GGRC component registry', function () {
  'use strict';

  var origStorage;  // the existing component private storage
  var Components;  // the component registry utility

  beforeAll(function () {
    Components = GGRC.Components;
  });

  beforeEach(function () {
    origStorage = Components._registry;
    Components._registry = {};
  });

  afterEach(function () {
    Components._registry = origStorage;
  });

  describe('using the Components registry as a function', function () {
    var componentConfig;
    var fakeComponent;

    beforeEach(function () {
      componentConfig = {
        tag: 'foo-bar',
        template: 'Hello World!'
      };
      fakeComponent = function FooBar() {};

      spyOn(can.Component, 'extend').and.returnValue(fakeComponent);
    });

    it('adds a new component to the registry', function () {
      delete Components._registry.foo;
      Components('foo', componentConfig);
      expect(Components._registry.foo).toBe(fakeComponent);
    });

    it('returns the newly created component', function () {
      var result;
      delete Components._registry.foo;
      result = Components('foo', componentConfig);
      expect(result).toBe(fakeComponent);
    });

    it('throws an error if a component is already registered', function () {
      var componentConfig = {};

      Components._registry.foo = function FooBar() {};

      expect(function () {
        Components('foo', componentConfig);
      })
      .toThrow(new Error('Component already exists: foo'));
    });

    it('throws an error if registering a component under a blank name',
      function () {
        var componentConfig = {};

        expect(function () {
          Components('', componentConfig);
        })
        .toThrow(new Error('Component name must be a nonempty string.'));
      }
    );

    it('throws an error if the given name is not a string', function () {
      var componentConfig = {};

      expect(function () {
        Components(123, componentConfig);
      })
      .toThrow(new Error('Component name must be a nonempty string.'));
    });
  });

  describe('unregister() method', function () {
    it('removes a component from the registry', function () {
      Components._registry.foo = function FooBar() {};
      Components.unregister('foo');
      expect(Components._registry.foo).toBeUndefined();
    });

    it('silently does nothing if a component does not exist', function () {
      delete Components._registry.foo;  // the "foo" component does not exist

      try {
        Components.unregister('foo');
      } catch (err) {
        fail('An error should not have be thrown.');
      }
    });
  });

  describe('isRegistered() method', function () {
    it('returns true if a component is registered', function () {
      Components._registry.foo = function FooBar() {};
      expect(Components.isRegistered('foo')).toBe(true);
    });

    it('returns false if a component is not registered', function () {
      delete Components._registry.foo;
      expect(Components.isRegistered('foo')).toBe(false);
    });
  });

  describe('get() method', function () {
    it('returns the component registered under the given name', function () {
      var componentFoo = function () {};
      Components._registry.foo = componentFoo;
      expect(Components.get('foo')).toBe(componentFoo);
    });

    it('raises an error if a component does not exist', function () {
      delete Components._registry.foo;

      expect(function () {
        Components.get('foo');
      })
      .toThrow(new Error('Component not found: foo'));
    });
  });
});
