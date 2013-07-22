/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

(function(can, $) {

can.Control("CMS.Controllers.Dashboard", {
    defaults: {
        widget_descriptors: null
      //, widget_listeners: null
      //, widget_containers: null
    }

}, {
    init: function(options) {
      if (!this.inner_nav_controller)
        this.inner_nav_controller = new CMS.Controllers.InnerNav(
          $(".inner-nav .internav"), { dashboard_controller: this });

      this.update_inner_nav();
    }

  , " widgets_updated" : "update_inner_nav"

  , " inner_nav_sort_updated": function(el, ev, widget_ids) {
        this.apply_widget_sort(widget_ids);
      }

  , apply_widget_sort: function(widget_ids) {
      var that = this
        ;

      can.each(this.get_active_widget_container_elements(), function(elem) {
        $(elem).trigger("apply_widget_sort", [widget_ids])
      });

      this.update_inner_nav();
    }

  , update_inner_nav: function(el, ev, data) {
      this.inner_nav_controller.update_widget_list(
        this.get_active_widget_elements());
    }

  , get_active_widget_container_elements: function() {
      return this.element.find(".widget-area").toArray();
    }

  , get_active_widget_elements: function() {
      return this.element.find("section.widget[id]:not([id=])").toArray();
    }

  , add_widget_from_descriptor: function() {
      var descriptor = {}
        , that = this
        ;

      // Construct the final descriptor from one or more arguments
      can.each(arguments, function(name_or_descriptor) {
        if (typeof(name_or_descriptor) === "string")
          name_or_descriptor = that.widget_descriptors[name_or_descriptor];
        $.extend(descriptor, name_or_descriptor || {});
      });

      // Create widget in container?
      //return this.options.widget_container[0].add_widget(descriptor);

      var $element = $("<section class='widget'>")
        , control = new descriptor.controller(
            $element, descriptor.controller_options)
        ;

      // FIXME: Abstraction violation: Sortable/DashboardWidget/ResizableWidget
      //   controllers should maybe handle this?
      var $container = $(this.get_active_widget_container_elements()[0])
        , $last_widget = $container.find('section.widget').last()
        ;

      $last_widget.after($element);
      $element
        .trigger("sortreceive")
        .trigger("section_created")
        .trigger("widgets_updated")

      return control;
    }

  , add_dashboard_widget_from_descriptor: function (descriptor) {
      return this.add_widget_from_descriptor({
        controller: CMS.Controllers.DashboardWidgets,
        controller_options: descriptor
      });
    }
});


can.Control("CMS.Controllers.InnerNav", {
  defaults: {
      internav_view : "/static/mustache/dashboard/internav_list.mustache"
    , widget_list : null
  }
}, {
    init: function(options) {
      var that = this
        ;

      if (!this.options.widget_list)
        this.options.widget_list = new can.Observe.List([]);

      this.sortable();

      can.view(this.options.internav_view, this.options, function(frag) {
        that.element.append(frag);
        that.update_scrollspy();
      });
    }

  , sortable: function() {
      return this.element.sortable({
          placeholder: 'drop-placeholder'
        , items : "li"
      })
    }

  , " sortupdate": "apply_widget_list_sort"

  , apply_widget_list_sort: function() {
      var widget_ids
        ;

      widget_ids = this.element.find("li > a").map(function() {
        return $(this).attr("href");
      }).toArray();

      this.element.trigger("inner_nav_sort_updated", [widget_ids]);
    }

  , replace_widget_list : function(widget_elements) {
      var widget_list = []
        ;

      can.each(widget_elements, function(widget_element) {
        var $widget = $(widget_element);
        widget_list.push({
            selector: "#" + $widget.attr("id")
          , internav_display: $widget.find(".header").text()
          });
      });
      this.options.widget_list.replace(widget_list);
    }

  , update_scrollspy : function() {
      var $body = $("body")
        , top = $body.scrollTop()
        ;

      // FIXME: This is currently necessary because Bootstrap's ScrollSpy uses
      //   the `href` to determine the active element, and the element may have
      //   changed (due to view update) while keeping the same `href`.
      // So, we nullify the "current" href.
      $body.data("scrollspy").activeTarget = null;
      $body
        .scrollTop(0)
        .scrollspy("refresh")
        .scrollTop(top)
        .scrollspy("process");
    }

  , update_widget_list : function(widget_elements) {
      this.replace_widget_list(widget_elements);
      this.update_scrollspy();
    }

});

})(this.can, this.can.$);
