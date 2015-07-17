/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

$(document).ready(function() {

  can.Component.extend({
    tag: "dashboard",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".dashboard-wrap").html(can.view("/static/mockups/mustache/dashboard.mustache",{}));
});
