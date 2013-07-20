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
  }
}, {
  
  init : function() {
    var that = this;
    if(!this.options.menu_tree) {
      this.options.is_related = true
      this.scrapeRelated();
    }

    can.view(this.options.menu_view, this.options.menu_tree, function(frag) {
      that.element.find(".dropdown-menu").html(frag).find(".divider:last").remove();
    });
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
          descriptor.object_display = descriptor.object_display;
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
    var that = this;
    if(descriptor && !$("#" + descriptor.object_type + "_widget").length) {
      $("<section class='widget'>")
      .insertBefore(that.element)
      .cms_controllers_dashboard_widgets({
        content_controller : GGRC.Controllers.ListView
        , content_controller_options : $.extend(descriptor, { is_related : this.options.is_related })
        , widget_id : descriptor.model.table_singular
        , widget_name : descriptor.model.title_plural
        , widget_icon : descriptor.model.table_singular
        , model : descriptor.model
        , object_category : descriptor.model.category || descriptor.object_category })
      .trigger("sortreceive");
    }
  }

  , addWidgetByName : function(widget_name) {
    this.addWidgetByDescriptor(this.options.widget_descriptors[widget_name]);
  }
});
