/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all

can.Control("CMS.Controllers.AddWidget", {
  defaults : {
    widget_descriptors : null
    , menu_tree : null
    , menu_view : GGRC.mustache_path + "/add_widget_menu.mustache"
    , minimum_widget_height : 100
    , is_related : false
    , parent_controller : null
  }
}, {
  
  init : function() {
    var that = this;

    can.each(this.options.widget_descriptors, function(descriptor, name) {
      that.options.widget_descriptors[name] =
        that.make_descriptor_from_model_descriptor(that.options.widget_descriptors[name]);
    });

    if(!this.options.menu_tree) {
      this.options.is_related = true
      this.scrapeRelated();
    }

    can.view(this.options.menu_view, this.options.menu_tree, function(frag) {
      that.element.find(".dropdown-menu").html(frag).find(".divider:last").remove();
    });
  }

  , make_descriptor_from_model_descriptor: function(descriptor) {
      if (descriptor.widget_id || !descriptor.model)
        return descriptor

      return {
        content_controller: GGRC.Controllers.ListView,
        content_controller_options: descriptor,
        widget_id: descriptor.model.table_singular,
        widget_name: descriptor.model.title_plural,
        widget_icon: descriptor.model.table_singular,
        object_category: descriptor.model.category || descriptor.object_category
      }
    }

  , scrapeRelated : function() {
      var that = this
        , page_model = GGRC.infer_object_type(GGRC.page_object).shortName
        , categories_index = {}
        ;

      this.options.menu_tree = {categories : []};

      can.each(GGRC.RELATIONSHIP_TYPES[page_model], function(value, key, root) {
        var related_model = CMS.Models[key]
          , descriptor = that.options.widget_descriptors[related_model.table_singular]
          ;

        if (descriptor) {
          if(!categories_index[descriptor.object_category]) {
            categories_index[descriptor.object_category] = {
                title : can.map(descriptor.object_category.split(" "), can.capitalize).join(" ")
              , objects : []
              };
            that.options.menu_tree.categories.push(categories_index[descriptor.object_category]);
          }
          categories_index[descriptor.object_category].objects.push(descriptor);
        }
      });
    }

  , ".dropdown-menu > * click" : function(el, ev) {
    var descriptor = this.options.widget_descriptors[el.attr("class")];
    this.addWidgetByDescriptor(descriptor);
  }

  , ".dropdown-toggle click" : function() {
      setTimeout(this.proxy("repositionMenu"), 10);
    }
  , "{window} resize" : "repositionMenu"
  , "{window} scroll" : "repositionMenu"

  , repositionMenu : function(el, ev) {
    var $dropdown = this.element.find(".dropdown-menu:visible")
    if(!$dropdown.length) 
      return;

    $dropdown.css({"position" : "", "top" : "", "bottom" : "" });
    //NOTE: if the position property of the dropdown toggle button is changed to "static" (it is current "relative"),
    //  this code will fail.  Please do not remove the relative positioning from ".dropdown-toggle" --BM 3/1/2013
    if($dropdown.offset().top < window.scrollY) {
      $dropdown.css({
        "position" : "absolute"
        , "top" : window.scrollY - this.element.find(".dropdown-toggle").offset().top
        , "bottom" : $(".dropdown-menu:visible").css("bottom", -window.scrollY - 443 + this.element.find(".dropdown-toggle").offset().top - this.element.find(".dropdown-toggle").height() ) 
      })
    }
  }

  , addWidgetByDescriptor : function(descriptor) {
      if (this.options.parent_controller) {
        // FIXME: This ought not change the persistent descriptor object!
        // FIXME: This must change before single page app can be accomplished
        descriptor.content_controller_options.is_related = this.options.is_related;

        this.options.parent_controller
          .add_dashboard_widget_from_descriptor(descriptor)
      }
    }

  , addWidgetByName : function(widget_name) {
      var descriptor = this.options.widget_descriptors[widget_name];
      if (!descriptor)
        // FIXME: This happens when previously-existing widgets no longer exist,
        //   but only the first time (then DisplayPrefs are overwritten correctly).
        return;
      this.addWidgetByDescriptor(descriptor);
  }
});
