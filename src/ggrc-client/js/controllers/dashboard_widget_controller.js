/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import canControl from 'can-control';
import {getDashboards} from '../plugins/utils/dashboards-utils';
import {
  getPageModel,
  getPageInstance,
} from '../plugins/utils/current-page-utils';

export default canControl.extend({
  defaults: {
    model: getPageModel(),
    instance: getPageInstance(),
    isLoading: true,
  },
}, {
  init: function () {
    let options = this.options;
    let dashboards = getDashboards(options.instance);
    let $element = $(this.element);

    options.context = new CanMap({
      model: options.model,
      instance: options.instance,
      dashboards: dashboards,
      activeDashboard: dashboards[0],
      showDashboardList: dashboards.length > 1,
      selectDashboard: function (dashboard) {
        this.attr('activeDashboard', dashboard);
      },
    });
    $.ajax({
      url: options.widget_view,
      dataType: 'text',
    }).then((view) => {
      let frag = can.stache(view)(options.context);
      $element.html(frag);
    });
    return 0;
  },
});
