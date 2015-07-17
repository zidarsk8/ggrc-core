$(document).ready(function() {

  can.Component.extend({
    tag: "export",
    template: "<content/>",
  });
  $(".export-info").html(can.view("/static/mockups/mustache/export/export-object.mustache",{}));

  can.Component.extend({
    tag: "export-control",
    template: "<content/>",
  });
  $(".export-control").html(can.view("/static/mockups/mustache/export/export-control-object.mustache",{}));

  function innerNavTrigger() {
    var $this = $(this),
        $allList = $this.closest(".nav").children("li"),
        $list = $this.closest("li"),
        aId = $this.attr("href"),
        $element = $("div"+aId);

    $(".export-content").hide();
    $(".export-content"+aId).show();
  }

  $(".top-inner-nav a").on("click", innerNavTrigger);

});
