$(document).ready(function() {

  can.Component.extend({
    tag: "risk-assessment-info",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-info").html(can.view("/static/mockups/mustache/risk-assessment/info.mustache",{}));

  can.Component.extend({
    tag: "heat-map",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-heat").html(can.view("/static/mockups/mustache/risk-assessment/heat.mustache",{}));

  can.Component.extend({
    tag: "risks",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-risks").html(can.view("/static/mockups/mustache/risk-assessment/risks.mustache",{}));

  can.Component.extend({
    tag: "people",
    scope: {
    },
    template: "<content/>",
    helpers: {
    },
    events: {
    }
  });
  $(".object-wrap-people").html(can.view("/static/mockups/mustache/risk-assessment/people.mustache",{}));

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

  function riskAssessmentGenerate() {
    $('#autoGenerateRA').modal('hide');
    $('#RAList').show();
    $('#removeLegend').hide();
  }

  $(".top-inner-nav a").on("click", innerNavTrigger);

  $("#autoGenerateRA").on("click", riskAssessmentGenerate);
});
