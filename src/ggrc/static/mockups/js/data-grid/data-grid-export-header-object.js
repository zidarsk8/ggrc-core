/*
 * Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: ivan@reciprocitylabs.com
 * Maintained By: ivan@reciprocitylabs.com
 */

$(document).ready(function() {

  can.Component.extend({
    tag: "reporting-header",
    scope: {
      report_gen: false,
    },
    template: "<content/>",
  });

  $(".title-content").html(can.view("/static/mockups/mustache/data-grid/data-grid-export-header-object.mustache",{}));
});
