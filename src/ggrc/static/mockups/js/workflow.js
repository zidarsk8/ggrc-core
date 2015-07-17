$(document).ready(function() {

  can.Component.extend({
    tag: "workflow",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/workflow.mustache",{}));
});
