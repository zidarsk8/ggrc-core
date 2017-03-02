/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('CMS.Controllers.TreeView', function () {
  'use strict';

  var Ctrl;  // the controller under test

  beforeAll(function () {
    Ctrl = CMS.Controllers.TreeView;
  });

  describe('init() method', function () {
    var ctrlInst;  // fake controller instance
    var dfdSingleton;
    var method;
    var options;
    var $element;

    beforeEach(function () {
      options = {};
      $element = $('<div></div>');

      ctrlInst = {
        element: $element,
        widget_hidden: jasmine.createSpy('widget_hidden'),
        widget_shown: jasmine.createSpy('widget_shown'),
        options: new can.Map(options)
      };

      method = Ctrl.prototype.init.bind(ctrlInst);

      dfdSingleton = new can.Deferred();
      spyOn(
        CMS.Models.DisplayPrefs, 'getSingleton'
      ).and.returnValue(dfdSingleton);
    });

    // test cases here...
  });

  describe('_verifyRelationship() method', function () {
    var ctrlInst;
    var method;
    var relationship;

    beforeEach(function () {
      ctrlInst = {
        options: new can.Map({
          model: {
            shortName: 'foo'
          }
        })
      };

      relationship = new CMS.Models.Relationship();

      method = Ctrl.prototype._verifyRelationship.bind(ctrlInst);
    });

    it('wrong relationship', function () {
      var result;

      relationship.source = {type: 'bar'};
      relationship.destination = {type: 'baz'};

      result = method(relationship, 'foo');

      expect(result).toBeFalsy();
    });

    it('right relationship', function () {
      var result;

      relationship.source = {type: 'bar'};
      relationship.destination = {type: 'foo'};

      result = method(relationship, 'foo');

      expect(result).toBeTruthy();
    });

    it('right relationship for Snapshot', function () {
      var result;

      relationship.source = {type: 'bar'};
      relationship.destination = {type: 'Snapshot'};

      result = method(relationship, 'foo');

      expect(result).toBeTruthy();
    });

    it('right relationship without source', function () {
      var result;

      relationship.destination = {type: 'foo'};

      result = method(relationship, 'foo');

      expect(result).toBeTruthy();
    });

    it('right relationship without destination', function () {
      var result;

      relationship.source = {type: 'foo'};

      result = method(relationship, 'foo');

      expect(result).toBeTruthy();
    });

    it('empty relationship', function () {
      var result;

      result = method(relationship, 'foo');

      expect(result).toBeFalsy();
    });
  });

  describe('update_header() method', function () {
    beforeEach(function () {
      Ctrl.prototype.options = new can.Map({
        model: {
          shortName: 'foo'
        },
        list: []
      });
      Ctrl.prototype.element = $('<div></div>');
      Ctrl.prototype.display_prefs = {
        setFilterHidden: function () {},
        save: function () {}
      };

      spyOn(Ctrl.prototype, 'update_header');
    });

    it('update_header() should be called after call of init_view()',
      function () {
        var initView = Ctrl.prototype.init_view.bind(Ctrl.prototype);

        initView();
        expect(Ctrl.prototype.update_header.calls.count()).toEqual(1);
      }
    );

    it('update_header() should be called after call of widget_shown()',
      function () {
        var widgetShown = Ctrl.prototype.widget_shown.bind(Ctrl.prototype);

        widgetShown();
        expect(Ctrl.prototype.update_header.calls.count()).toEqual(1);
      }
    );

    it('update_header() should be called after call of add_child_lists()',
      function () {
        var addChildLists = Ctrl.prototype.add_child_lists.bind(Ctrl.prototype);

        addChildLists([]);
        expect(Ctrl.prototype.update_header.calls.count()).toEqual(1);
      }
    );
  });
});
