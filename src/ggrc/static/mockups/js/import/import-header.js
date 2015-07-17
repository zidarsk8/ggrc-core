$(document).ready(function() {

  can.Component.extend({
    tag: "header",
    scope: {
      report_gen: false,
    },
    template: "<content/>",
  });

  $(".title-content").html(can.view("/static/mockups/mustache/import/import-header.mustache",{}));
});
