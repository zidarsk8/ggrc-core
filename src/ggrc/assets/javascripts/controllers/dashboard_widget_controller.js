/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  can.Control('GGRC.Controllers.DashboardWidget', {
    defaults: {
      model: null,
      instance: null,
      widget_view: GGRC.mustache_path + '/base_objects/dashboard.mustache',
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
      var frag;
      if (this.element.data('widget-view')) {
        this.options.widget_view = GGRC.mustache_path +
          this.element.data('widget-view');
      }
      this.options.context = new can.Map({
        model: this.options.model,
        instance: this.options.instance,
        dashboardUrl: GGRC.Utils.Dashboards.getDashboardUrl(
          this.options.model.table_singular,
          this.options.instance
        )
      });
      frag = can.view(this.get_widget_view(this.element),
                      this.options.context);
      this.element.html(frag);
      return 0;
    },
    get_widget_view: function (el) {
      var widgetView = $(el)
        .closest('[data-widget-view]')
        .attr('data-widget-view');
      return (widgetView && widgetView.length > 0) ?
          GGRC.mustache_path + widgetView :
          this.options.widget_view;
    }
  });
})(this.can, this.can.$);
