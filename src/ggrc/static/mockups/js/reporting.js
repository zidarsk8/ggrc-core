$(document).ready(function() {

  can.Component.extend({
    tag: "reporting",
    scope: {
      test: "hello"
    },
    template: "<content/>",
    helpers: {
    },
    events: {
      "#newReportAdd click": function(el, ev) {
        // this.element is the <reporting>...</reporting> element
        var $reportTab = this.element.find("#newReport");
        $reportTab.show().addClass("active");
      },
      "#custom_report_name keyup": function(el, ev) {
        this.element.find("#newReport a .oneline .title").text("Controls Review");
        this.element.find("#newReport .closed").show();
      },
      ".report-trigger click": function(el, ev) {
        this.element.find("#zeroState").fadeOut(500);
        this.element.find("#generatedReport").delay(500).fadeIn(500);
      }
    }
  });

  $(".area").html(can.view("/static/mockups/mustache/reporting.mustache",{}));
});
