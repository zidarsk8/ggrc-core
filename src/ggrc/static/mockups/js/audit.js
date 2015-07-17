$(document).ready(function() {

  can.Component.extend({
    tag: "audit",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/audit.mustache",{}));
});
