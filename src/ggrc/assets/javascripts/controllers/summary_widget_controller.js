/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  can.Control('GGRC.Controllers.SummaryWidget', {
    defaults: {
      model: null,
      instance: null,
      widget_view: GGRC.mustache_path + '/base_objects/summary.mustache',
      isLoading: true
    },
    init: function () {
      var that = this;
      $(function () {
        if (GGRC.page_object) {
          $.extend(that.defaults, {
            model: GGRC.infer_object_type(GGRC.page_object),
            instance: GGRC.page_instance()
          });
        }
      });
    }
  }, {
    init: function () {
      var that = this;
      if (this.element.data('widget-view')) {
        this.options.widget_view = GGRC.mustache_path +
          this.element.data('widget-view');
      }
      this.element.closest('.widget')
        .on('widget_shown', this.widget_shown.bind(this));
      this.element.closest('.widget')
        .on('widget_hidden', this.widget_hidden.bind(this));
      this.options.context = new can.Map({
        model: this.options.model,
        instance: this.options.instance,
        error_msg: '',
        error: true
      });
      can.view(this.get_widget_view(this.element),
        this.options.context, function (frag) {
          that.element.html(frag);
        });
      return 0;
    },
    get_widget_view: function (el) {
      var widgetView = $(el)
        .closest('[data-widget-view]')
        .attr('data-widget-view');
      return (widgetView && widgetView.length > 0) ?
          GGRC.mustache_path + widgetView :
          this.options.widget_view;
    },
    widget_shown: function (event) {
      setTimeout(this.reloadSummary.bind(this), 0);
      return false;
    },
    widget_hidden: function (event) {
      this.setState('requests', {total: 0, statuses: { }}, true);
      this.setState('assessments', {total: 0, statuses: { }}, true);
      return false;
    },
    reloadSummary: function () {
      var that = this;
      this.loadChartLibrary(function () {
        that.reloadChart('Assessment', 'assessments',
          'piechart_audit_assessments_chart');
        that.reloadChart('Request', 'requests',
          'piechart_audit_requests_chart');
      });
    },
    reloadChart: function (type, name, elementId) {
      var that = this;
      that.setState(name, {total: 0, statuses: { }}, true);
      that.getStatuses(type, that.options.instance.id).then(function (raw) {
        var data = that.parseStatuses(raw[0][type]);
        that.drawChart(elementId, data);
        that.setState(name, data, false);
      });
    },
    drawChart: function (elementId, raw) {
      var columns = [['Status', 'Count']];
      var data;
      var chart;
      var options = this.getChartOptions(raw);
      columns.push.apply(columns, raw.statuses);
      data = google.visualization.arrayToDataTable(columns);
      chart = new google.visualization.PieChart(
        document.getElementById(elementId));
      chart.draw(data, options);
      this.resizeChart(chart, data, options);
    },
    getChartOptions: function (raw) {
      var options = {
        pieSliceText: 'value-and-percentage',
        chartArea: {
          width: '100%',
          height: '90%'
        },
        legend: {
          position: 'right',
          alignment: 'center'
        }
      };
      var colorMaps = {
        Completed: '#8bc34a',
        'In Progress': '#ffab40',
        'Not Started': '#bdbdbd',
        Verified: '#1378bb'
      };
      options.colors = raw.statuses.map(function (e) {
        return colorMaps[e[0]];
      });
      return options;
    },
    resizeChart: function (chart, data, options) {
      $(window).resize(function () {
        chart.draw(data, options);
      });
      setTimeout(function () {
        $(window).trigger('resize');
      }, 0);
    },
    setState: function (name, data, isLoading) {
      var instance = this.options.context.instance;
      instance.attr(name + '_total', data.total);
      instance.attr(name + '_any', data.total > 0);
      instance.attr(name + '_none', isLoading || data.total === 0);
      instance.attr(name + '_isLoading', isLoading);
      instance.attr(name + '_isLoaded', !isLoading);
    },
    parseStatuses: function (data) {
      var groups = _.groupBy(data.values, 'status');
      var pairs = _.pairs(groups);
      var sorted = _.sortBy(pairs, function (e) {
        return e[0];
      });
      var result = sorted.map(function (e) {
        var name = e[0];
        var count = e[1].length;
        return [name, count];
      });
      return {
        total: data.total,
        statuses: result
      };
    },
    getStatuses: function (type, auditId) {
      var query = GGRC.Utils.QueryAPI.buildParam(
        type,
        {},
        {id: auditId, type: 'Audit'},
        ['status']);
      return GGRC.Utils.QueryAPI.makeRequest({data: [query]});
    },
    loadChartLibrary: function (callback) {
      if (typeof google !== 'undefined' &&
          typeof google.charts !== 'undefined') {
        callback();
        return;
      }
      GGRC.Utils.loadScript('https://www.gstatic.com/charts/loader.js', function () {
        google.charts.load('45', {packages: ['corechart']});
        google.charts.setOnLoadCallback(callback);
      });
    }
  });
})(this.can, this.can.$);
