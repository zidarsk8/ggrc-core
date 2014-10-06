$(document).ready(function() {

  can.Component.extend({
    tag: "reporting",
    scope: {
      pivot_selected: false,
      tabs: [
        {title: "ISO Systems"},
        {title: "Overdue tasks"},
      ]
    },
    template: "<content/>",
    helpers: {
    },
    events: {
      "#custom_report_name keyup": function(el, ev) {
        var $item = this.element.find('li.active'),
            index = $item.index(),
            tabs = this.scope.tabs;

        tabs[index].attr('title', el.val());
        this.element.find("#newReport .closed").show();
      },
      ".report-trigger click": function(el, ev) {
        this.element.find("#zeroState").fadeOut(500);
        this.element.find("#generatedReport").delay(500).fadeIn(500);
      },
      "#pivot_search keyup": function(el, ev) {
        var search = el.val();
        this.scope.attr('pivot_selected', search.trim() !== "");
      },
      "#newReportAdd click": function(el, ev) {
        var tabs = this.scope.tabs,
            new_tabs = 1,
            $ul = el.closest('ul');
        tabs.forEach(function(tab) {
          if (tab.new_report) {
            new_tabs++;
          }
        });
        tabs.push({title: "New Report " + new_tabs, new_report: true});
        $ul.find('li').not('.hidden-widgets-list').last().addClass("active");
      },
    }
  });

  $(".area").html(can.view("/static/mockups/mustache/reporting.mustache",{}));
});
