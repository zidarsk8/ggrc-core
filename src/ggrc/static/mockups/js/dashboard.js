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
