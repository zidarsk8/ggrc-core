$(document).ready(function() {

  can.Component.extend({
    tag: "object",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/object.mustache",{}));
});
