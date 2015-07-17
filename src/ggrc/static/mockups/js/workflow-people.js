$(document).ready(function() {

  can.Component.extend({
    tag: "workflowPeople",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/workflow-people.mustache",{}));
});
