$(document).ready(function() {

  can.Component.extend({
    tag: "reporting",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".area").html(can.view("/static/mockups/mustache/reporting.mustache",{}));
});
