$(document).ready(function() {

  can.Component.extend({
    tag: "import",
    scope: {
      report_gen: false,
    },
    template: "<content/>",
    helpers: {
    },
    events: {}
  });

  $(".import-content").html(can.view("/static/mockups/mustache/import-export.mustache",{}));
});
