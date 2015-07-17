$(document).ready(function() {

  can.Component.extend({
    tag: "tree",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/tree.mustache",{}));
});
