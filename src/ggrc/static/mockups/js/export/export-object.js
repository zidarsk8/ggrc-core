/*
 * Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: ivan@reciprocitylabs.com
 * Maintained By: ivan@reciprocitylabs.com
 */

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
