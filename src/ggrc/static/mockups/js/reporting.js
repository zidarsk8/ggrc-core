$(document).ready(function() {

  can.Component.extend({
    tag: "reporting",
    scope: {
      pivot_selected: false,
      //attr_selected: false,
      tabs: [
        {title: "ISO Systems"},
        {title: "Overdue tasks"},
      ]
      /*
      attr_select: function() {
        $(".attribute-trigger").popover({
          container: "body",
          html: true,
          content: function(){
            return $(this).next('.attr-wrap').html();
          },
          placement: "bottom",
          template: '<div class="popover" role="tooltip"><div class="popover-content"></div></div>'
        });

        $('.attribute-trigger').on('shown.bs.popover', function () {
          $(this).addClass("active");
        });

        $('.attribute-trigger').on('hidden.bs.popover', function () {
          $(this).removeClass("active");
        });
      }
      */
    },
    template: "<content/>",
    helpers: {
    },
    events: {
      "#custom_report_name keyup": function(el, ev) {
        var $item = this.element.find('li.active'),
            index = $item.index(),
            tabs = this.scope.tabs,
            new_tabs = 0;

        tabs[index].attr('title', el.val());
        this.element.find("#newReport .closed").show();
        
        // Calculate tabs numbers
        tabs.forEach(function(tab) {
          if (tab.new_report) {
            new_tabs++;
          }
        });

        // Revert "New Report n" if custom_report_name is empty
        if (tabs[index].attr('title').trim() === "") {
          tabs[index].attr('title', "New Report " + new_tabs);
        }
      },
      ".report-trigger click": function(el, ev) {
        this.element.find(".zero-state").fadeOut(500);
        this.element.find(".generated-report").delay(500).fadeIn(500);
      },
      "#pivot_search keyup": function(el, ev) {
        var search = el.val();
        
        this.scope.attr('pivot_selected', search.trim() !== "");
        this.scope.attr('obj_title', search.toUpperCase());
        this.element.find(".selected-object").fadeIn(500);
        if (search.trim() === "") {
          this.element.find(".selected-object").fadeOut(500);
        }
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
      /*
      ".sec-obj change": function(el, ev) {
        var choose = el.val();
        if(choose === "System") {
          this.scope.attr('attr_selected', true);
          this.scope.attr_select();
        }
      },
      */
    }
  });

  $(".area").html(can.view("/static/mockups/mustache/reporting.mustache",{}));
});
