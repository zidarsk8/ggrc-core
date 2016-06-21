/*!
  Copyright (C) 2016 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.personItem', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('personItem');
  });

  describe('defining default scope values', function () {
    var scope;

    beforeAll(function () {
      scope = Component.prototype.scope;
    });

    it('sets the personObj to null', function () {
      expect(scope.personObj).toBeNull();
    });
  });

  describe('init() method', function () {
    var dfdFindOne;
    var template;  // the DOM element passed to the component instance
    var origPersonCache;
    var component;
    var frag;

    beforeEach(function () {
      dfdFindOne = new can.Deferred();
      spyOn(CMS.Models.Person, 'findOne').and.returnValue(dfdFindOne);

      origPersonCache = CMS.Models.Person.cache;
      CMS.Models.Person.cache = {};
    });

    afterEach(function () {
      CMS.Models.Person.cache = origPersonCache;
    });

    it('sets the personObj in scope to the cached Person object ' +
      'if found there',
      function () {
        var person42 = new can.Map({
          id: 42, name: 'John', email: 'john@doe.com'
        });
        CMS.Models.Person.cache[42] = person42;

        template = can.view.mustache('<person person-id="42"></person>');
        frag = template();
        frag = $(frag);
        component = frag.find('person').control();

        expect(component.scope.attr('personObj')).toBe(person42);
      }
    );

    it('sets the personObj in scope to the fetched Person object ' +
      'if not found in cache',
      function () {
        var person123 = new can.Map({
          id: 123, name: 'Mike', email: 'mike@mike.com'
        });

        template = can.view.mustache('<person person-id="123"></person>');
        frag = template();

        frag = $(frag);
        component = frag.find('person').control();

        delete CMS.Models.Person.cache[123];

        dfdFindOne.resolve(person123);

        expect(CMS.Models.Person.findOne).toHaveBeenCalledWith({id: 123});
        expect(component.scope.attr('personObj')).toBe(person123);
      }
    );

    it('sets the personObj in scope to the fetched Person object ' +
      'for partially loaded objects in cache',
      function () {
        var person123 = new can.Map({id: 123, name: '', email: ''});
        var fetchedPerson = new can.Map({
          id: 123, name: 'John', email: 'john@doe.com'
        });

        template = can.view.mustache('<person person-id="123"></person>');
        frag = template();

        CMS.Models.Person.cache[123] = person123;

        frag = $(frag);
        component = frag.find('person').control();

        dfdFindOne.resolve(fetchedPerson);

        expect(CMS.Models.Person.findOne).toHaveBeenCalledWith({id: 123});
        expect(component.scope.attr('personObj')).toBe(fetchedPerson);
      }
    );
  });

  describe('unmap person click event handler', function () {
    var handler;  // the event handler under test
    var componentInst;  // fake component instance

    beforeAll(function () {
      handler = Component.prototype.events['a.unmap click'];
    });

    beforeEach(function () {
      componentInst = {
        element: {
          triggerHandler: jasmine.createSpy()
        },
        scope: new can.Map()
      };

      handler = handler.bind(componentInst);
    });

    it('triggers the person-remove event with the person object as the ' +
      'event argument',
      function () {
        var call;
        componentInst.scope.attr('personObj', {id: 123, name: 'John'});

        handler();

        expect(componentInst.element.triggerHandler).toHaveBeenCalled();
        call = componentInst.element.triggerHandler.calls.mostRecent();
        expect(call.args[0].type).toEqual(
          Component.prototype._EV_REMOVE_CLICK);
        expect(call.args[0].person.attr()).toEqual({id: 123, name: 'John'});
      }
    );
  });
});
