/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('CMS.Controllers.InnerNav', function () {
  'use strict';

  var Ctrl;  // the controller under test

  beforeAll(function () {
    Ctrl = CMS.Controllers.InnerNav;
  });

  describe('sortWidgets() method', function () {
    var ctrlInst;  // fake controller instance
    var sortWidgets;
    var options;

    beforeEach(function () {
      options = {
        widget_list: new can.Observe.List([])
      };

      ctrlInst = {
        options: new can.Map(options)
      };

      sortWidgets = Ctrl.prototype.sortWidgets.bind(ctrlInst);
    });

    it('sorts widgets by their "order" attribute', function () {
      var widgetOrder;
      var widgets = [
        {internav_display: 'aaa', order: 40},
        {internav_display: 'bbb', order: 20},
        {internav_display: 'ccc', order: 50},
        {internav_display: 'ddd', order: 10},
        {internav_display: 'eee', order: 30}
      ];
      options.widget_list.replace(widgets);

      sortWidgets();

      widgetOrder = _.map(ctrlInst.options.widget_list, 'internav_display');
      expect(widgetOrder).toEqual(['ddd', 'bbb', 'eee', 'aaa', 'ccc']);
    });

    it('places widgets with unknown "order" at the end and sort them in alphabetical order', function () {
      var widgetOrder;
      var widgets = [
        {internav_display: 'abc'},
        {internav_display: 'aaa', order: 40},
        {internav_display: 'cba'},
        {internav_display: 'ccc', order: 50},
        {internav_display: 'qwerty'},
        {internav_display: 'ddd', order: 10},
        {internav_display: 'xyz'},
        {internav_display: 'eee', order: 30}
      ];
      options.widget_list.replace(widgets);

      sortWidgets();

      widgetOrder = _.map(ctrlInst.options.widget_list, 'internav_display');
      expect(widgetOrder)
        .toEqual(['ddd', 'eee', 'aaa', 'ccc', 'abc', 'cba', 'qwerty', 'xyz']);
    });
  });

  describe('show_hide_titles() method', function () {
    var DISPLAY_WIDTH = 1920;
    var ctrlInst;  // fake controller instance
    var showHideTitles;
    var options;

    function createWidgets(titlesStatus) {
      var widgets = [
        {name: 'aaa', show_title: titlesStatus},
        {name: 'bbb', show_title: titlesStatus},
        {name: 'ccc', show_title: titlesStatus},
        {name: 'ddd', show_title: titlesStatus},
        {name: 'eee', show_title: titlesStatus},
        {name: 'fff', show_title: titlesStatus}
      ];
      options.attr('widget_list', widgets);
      return widgets;
    }

    function setWidgetsWidth(first, second) {
      spyOn(Array.prototype, 'reduce').and.returnValues(first, second);
    }

    beforeEach(function () {
      options = new can.Map({
        widget_list: new can.Observe.List([]),
        dividedTabsMode: false,
        priorityTabs: null
      });

      ctrlInst = {
        element: {
          children: jasmine.createSpy(),
          width: jasmine.createSpy().and.returnValue(DISPLAY_WIDTH)
        },
        options: options
      };

      spyOn(_, 'map')
        .and
        .returnValue([]);

      showHideTitles = Ctrl.prototype.show_hide_titles.bind(ctrlInst);
    });

    afterEach(function () {
      Array.prototype.reduce.calls.reset();
    });

    it('doesnt hide titles if the width is enough', function () {
      createWidgets(false);

      setWidgetsWidth(1500);

      showHideTitles();

      expect(_.every(options.attr('widget_list'), 'show_title')).toBeTruthy();
    });

    it('hides titles if the width isnt enough', function () {
      createWidgets(true);

      setWidgetsWidth(2500);

      showHideTitles();

      expect(_.every(options.widget_list, 'show_title', false)).toBeTruthy();
    });

    it('hides not priority titles if the width isnt enough', function () {
      var widgetList;
      createWidgets(true);

      options.attr('dividedTabsMode', true);
      options.attr('priorityTabs', 3);

      setWidgetsWidth(2500, 1500);

      showHideTitles();

      widgetList = options.attr('widget_list');

      expect(_.every(widgetList.slice(0, 3), 'show_title')).toBeTruthy();
      expect(_.every(widgetList.slice(3), 'show_title', false)).toBeTruthy();
    });

    it('hides all titles if the width isnt enough', function () {
      var widgetList;
      createWidgets(true);

      options.attr('dividedTabsMode', true);
      options.attr('priorityTabs', 3);

      setWidgetsWidth(3000, 2000);

      showHideTitles();

      widgetList = options.attr('widget_list');

      expect(_.every(widgetList, 'show_title', false)).toBeTruthy();
    });
  });
});
