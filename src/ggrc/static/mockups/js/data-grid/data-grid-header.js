$(document).ready(function() {

  can.Component.extend({
    tag: "reporting-header",
    scope: {
      report_gen: false,
    },
    template: "<content/>",
  });

  $(".title-content").html(can.view("/static/mockups/mustache/data-grid/data-grid-header.mustache",{}));
});
