$(document).ready(function() {

  can.Component.extend({
    tag: "ca",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/audit-revamp/control-assessments.mustache",{}));
});
