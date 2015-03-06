$(document).ready(function() {

  can.Component.extend({
    tag: "audit-info",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-info").html(can.view("/static/mockups/mustache/audit-revamp/info.mustache",{}));

  can.Component.extend({
    tag: "control",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-control").html(can.view("/static/mockups/mustache/audit-revamp/control.mustache",{}));

  can.Component.extend({
    tag: "ca",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-ca").html(can.view("/static/mockups/mustache/audit-revamp/control-assessments.mustache",{}));

  function innerNavTrigger() {
    var $this = $(this),
        $allList = $this.closest(".nav").children("li"),
        $list = $this.closest("li"),
        aId = $this.attr("href"),
        $element = $("div"+aId);

    $allList.removeClass('active');
    $list.addClass('active');

    $(".object-wrap").hide();
    $(".object-wrap"+aId).show();
  }

  $(".top-inner-nav a").on("click", innerNavTrigger);

  $("#autoGenerateCA").on("click", function() {
    $("#ca .content").find(".tree-structure").find(".tree-item").show();
    $("#ca .content").find(".tree-structure").find(".zero-state").hide();
  });

});
