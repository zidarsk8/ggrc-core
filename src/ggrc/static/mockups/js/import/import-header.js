/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

$(document).ready(function() {

  can.Component.extend({
    tag: "header",
    scope: {
      report_gen: false,
    },
    template: "<content/>",
  });

  $(".title-content").html(can.view("/static/mockups/mustache/import/import-header.mustache",{}));
});
