$(document).ready(function() {

  can.Component.extend({
    tag: "auditInfo",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/audit-info.mustache",{}));
});
