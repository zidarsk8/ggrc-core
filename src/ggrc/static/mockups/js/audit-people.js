$(document).ready(function() {

  can.Component.extend({
    tag: "auditPeople",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });

  $(".object-wrap").html(can.view("/static/mockups/mustache/audit-people.mustache",{}));
});
