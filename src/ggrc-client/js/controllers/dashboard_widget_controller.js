/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getDashboards} from '../plugins/utils/dashboards-utils';
import {
  getPageModel,
  getPageInstance,
} from '../plugins/utils/current-page-utils';

export default can.Control({
  defaults: {
    model: getPageModel(),
    instance: getPageInstance(),
    isLoading: true,
  },
}, {
  init: function () {
    let frag;
    let dashboards =
      getDashboards(this.options.instance);

    this.options.context = new can.Map({
      model: this.options.model,
      instance: this.options.instance,
      dashboards: dashboards,
      activeDashboard: dashboards[0],
      showDashboardList: dashboards.length > 1,
      selectDashboard: function (dashboard) {
        this.attr('activeDashboard', dashboard);
      },
    });

    frag = can.view(this.options.widget_view,
      this.options.context);
    this.element.html(frag);
    return 0;
  },
});
