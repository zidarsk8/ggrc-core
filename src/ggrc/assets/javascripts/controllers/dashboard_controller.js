/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

(function(can, $) {

can.Control("CMS.Controllers.Dashboard", {
    defaults: {
        model_descriptors: null
      , menu_tree_spec: null
      //  widget_descriptors: null
      //, widget_listeners: null
      //, widget_containers: null
      //
    }

}, {
    init: function(options) {
      this.init_widget_descriptors();
      if (!this.options.menu_tree)
        this.init_menu_tree();
      if (!this.inner_nav_controller)
        this.init_inner_nav();
      this.update_inner_nav();
      if (!this.add_widget_controller)
        this.init_add_widget();
      if (!this.widget_area_controller)
        this.init_widget_area();
      this.init_default_widgets();
    }

  , init_widget_area: function() {
      this.widget_area_controller = new CMS.Controllers.SortableWidgets(
          this.element.find('.widget-area'), {
              dashboard_controller: this
          });
    }

  , init_inner_nav: function() {
      this.inner_nav_controller = new CMS.Controllers.InnerNav(
          this.element.find('.internav'), {
              dashboard_controller: this
          });
    }

  , init_add_widget: function() {
      this.add_widget_controller = new CMS.Controllers.AddWidget(
          this.element.find('.add-nav-item'), {
              dashboard_controller : this
            //, widget_descriptors : this.options.widget_descriptors
            , menu_tree : this.options.menu_tree
          });
      }

  , init_widget_descriptors: function() {
      var that = this;

      this.options.widget_descriptors = this.options.widget_descriptors || {};

      can.each(this.options.model_descriptors, function(descriptor, key) {
        that.options.widget_descriptors[key] =
          that.make_list_view_descriptor_from_model_descriptor(descriptor);
      });
    }

  , init_menu_tree: function() {
      var that = this
        , menu_tree = { categories: [] };

      can.each(this.options.menu_tree_spec, function(category) {
        var objects = can.map(category.objects, function(widget_name) {
          return that.options.widget_descriptors[widget_name];
        });

        menu_tree.categories.push({
            title: category.title
          , objects: objects
        });
      });

      this.options.menu_tree = menu_tree;
    }

  , init_default_widgets: function() {
      var that = this
        ;

      can.each(this.options.default_widgets, function(name) {
        var descriptor = that.options.widget_descriptors[name]
          ;

        that.add_dashboard_widget_from_descriptor(descriptor);
      });
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
          name_or_descriptor =
            that.options.widget_descriptors[name_or_descriptor];
        $.extend(descriptor, name_or_descriptor || {});
      });

      // Create widget in container?
      //return this.options.widget_container[0].add_widget(descriptor);

      if ($('#' + descriptor.controller_options.widget_id + '_widget').length > 0)
        return;

      // FIXME: This should be in some Widget superclass
      if (descriptor.controller_options.widget_guard
          && !descriptor.controller_options.widget_guard())
        return;

      var $element = $("<section class='widget'>")
        , control = new descriptor.controller(
            $element, descriptor.controller_options)
        ;

      // FIXME: Abstraction violation: Sortable/DashboardWidget/ResizableWidget
      //   controllers should maybe handle this?
      var $container = $(this.get_active_widget_container_elements()[0])
        , $last_widget = $container.find('section.widget').last()
        ;

      if ($last_widget.length > 0)
        $last_widget.after($element);
      else
        $container.append($element);

      $element
        .trigger("sortreceive")
        .trigger("section_created")
        .trigger("widgets_updated")

      return control;
    }

  , add_dashboard_widget_from_descriptor: function(descriptor) {
      return this.add_widget_from_descriptor({
        controller: CMS.Controllers.DashboardWidgets,
        controller_options: $.extend(descriptor, { dashboard_controller: this })
      });
    }

  , add_dashboard_widget_from_name: function(name) {
      var descriptor = this.options.widget_descriptors[name];
      if (!descriptor)
        console.debug("Unknown descriptor: ", name);
      else
        return this.add_dashboard_widget_from_descriptor(descriptor);
    }


  , make_list_view_descriptor_from_model_descriptor: function(descriptor) {
      return {
        content_controller: GGRC.Controllers.ListView,
        content_controller_options: descriptor,
        widget_id: descriptor.model.table_singular,
        widget_name: descriptor.model.title_plural,
        widget_icon: descriptor.model.table_singular,
        object_category: descriptor.model.category || descriptor.object_category
      }
    }
});


CMS.Controllers.Dashboard("CMS.Controllers.PageObject", {

}, {
    init: function() {
      this.options.model = this.options.instance.constructor;
      this._super();
      this.init_related_widgets();
    }

  , init_related_widgets: function() {
      var that = this
        , model_name = this.options.instance.constructor.shortName
        , relationships = GGRC.RELATIONSHIP_TYPES[model_name]
        ;

      can.each(relationships, function(value, key) {
        var related_model = CMS.Models[key]
          , descriptor = that.options.widget_descriptors[related_model.table_singular]
          ;

        that.add_dashboard_widget_from_descriptor(descriptor);
      });
    }

  , init_widget_descriptors: function() {
      var that = this;

      this.options.widget_descriptors = this.options.widget_descriptors || {};

      can.each(this.options.model_descriptors, function(descriptor, key) {
        that.options.widget_descriptors[key] =
          that.make_related_descriptor_from_model_descriptor(descriptor);
      });
    }

  , make_related_descriptor_from_model_descriptor: function(descriptor) {
      descriptor = this.make_list_view_descriptor_from_model_descriptor(descriptor);
      descriptor = $.extend({}, descriptor);
      descriptor.content_controller_options =
        $.extend({}, descriptor.content_controller_options);
      descriptor.content_controller_options.is_related = true;
      return descriptor;
    }

  , init_menu_tree: function() {
      var that = this
        , widget_descriptors = this.options.widget_descriptors
        , model_name = this.options.instance.constructor.shortName
        , categories_index = {}
        , menu_tree = { categories : [] }
        ;

      can.each(GGRC.RELATIONSHIP_TYPES[model_name], function(value, key) {
        var related_model = CMS.Models[key]
          , descriptor = widget_descriptors[related_model.table_singular]
          , category = null
          ;

        if (descriptor) {
          category = descriptor.object_category;

          if (!categories_index[category]) {
            categories_index[category] = {
                title : can.map(category.split(" "), can.capitalize).join(" ")
              , objects : []
              };
            menu_tree.categories.push(categories_index[category]);
          }
          categories_index[category].objects.push(descriptor);
        }
      });

      this.options.menu_tree = menu_tree;
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
          , internav_icon: $widget.find(".header h2 i").attr("class")
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
