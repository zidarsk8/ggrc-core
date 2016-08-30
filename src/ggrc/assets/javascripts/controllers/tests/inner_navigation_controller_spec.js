/*!
  Copyright (C) 2016 Google Inc.
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
        {widget_id: 'aaa', order: 40},
        {widget_id: 'bbb', order: 20},
        {widget_id: 'ccc', order: 50},
        {widget_id: 'ddd', order: 10},
        {widget_id: 'eee', order: 30}
      ];
      options.widget_list.replace(widgets);

      sortWidgets();

      widgetOrder = _.map(ctrlInst.options.widget_list, 'widget_id');
      expect(widgetOrder).toEqual(['ddd', 'bbb', 'eee', 'aaa', 'ccc']);
    });

    it('places widgets with unknown "order" at the end', function () {
      var lastWidget;
      var widgets = [
        {widget_id: 'aaa', order: 40},
        {widget_id: 'bbb', order: undefined},
        {widget_id: 'ccc', order: 50},
        {widget_id: 'ddd', order: 10},
        {widget_id: 'eee', order: 30}
      ];
      options.widget_list.replace(widgets);

      sortWidgets();

      lastWidget = ctrlInst.options.widget_list[4];
      expect(lastWidget.widget_id).toEqual('bbb');
    });
  });
});
