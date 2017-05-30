/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Controllers.SummaryWidget', function () {
  'use strict';
  var Ctrl;

  beforeAll(function () {
    Ctrl = GGRC.Controllers.SummaryWidget;
  });

  describe('widget_shown(event) method', function () {
    var method;
    var ctrlInst;
    var resizeHandler;

    beforeEach(function () {
      ctrlInst = {
        widget_shown: jasmine.createSpy('widget_shown'),
        reloadSummary: jasmine.createSpy('reloadSummary'),
        options: {
          context: new can.Map({})
        }
      };
      method = Ctrl.prototype.widget_shown.bind(ctrlInst);
      resizeHandler = jasmine.createSpy('resizeHandler');
      $(window).resize(resizeHandler);
    });

    afterEach(function () {
      $(window).off('resize', resizeHandler);
    });

    it('returns false', function () {
      var result = method();
      expect(result).toBe(false);
    });

    it('sets isShown option to true', function () {
      method();
      expect(ctrlInst.options.isShown).toBe(true);
    });

    it('dispatches resize event', function () {
      method();
      expect(resizeHandler).toHaveBeenCalledTimes(1);
    });
  });

  describe('widget_hidden(event) method', function () {
    var method;
    var ctrlInst;

    beforeEach(function () {
      ctrlInst = {
        widget_hidden: jasmine.createSpy('widget_hidden'),
        options: {
          context: new can.Map({})
        }
      };
      method = Ctrl.prototype.widget_hidden.bind(ctrlInst);
    });

    it('returns false', function () {
      var result = method();
      expect(result).toBe(false);
    });

    it('sets isShown option to false', function () {
      method();
      expect(ctrlInst.options.isShown).toBe(false);
    });
  });

  describe('"{window} resize" handler', function () {
    var method;
    var ctrlInst;
    var chart;

    beforeEach(function () {
      chart = {
        draw: jasmine.createSpy()
      };
      ctrlInst = {
        options: {
          chart: chart,
          chartOptions: 'options',
          data: 'data',
          isShown: true
        }
      };
      method = Ctrl.prototype['{window} resize'].bind(ctrlInst);
    });

    it('draws chart if summary widget is shown ' +
    'and chart, data, and chart options is defined', function () {
      method();
      expect(chart.draw).toHaveBeenCalledWith('data', 'options');
    });

    it('does not draw chart if summary widget is not shown', function () {
      ctrlInst.options.isShown = false;
      method();
      expect(chart.draw).not.toHaveBeenCalled();
    });
    it('does not draw chart if chart data is undefined', function () {
      ctrlInst.options.data = undefined;
      method();
      expect(chart.draw).not.toHaveBeenCalled();
    });
    it('does not draw chart if chart options is undefined', function () {
      ctrlInst.options.chartOptions = undefined;
      method();
      expect(chart.draw).not.toHaveBeenCalled();
    });
  });
});
