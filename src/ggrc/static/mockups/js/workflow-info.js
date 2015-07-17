$(document).ready(function() {

  can.Component.extend({
    tag: "workflowInfo",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/workflow-info.mustache",{}));
});

