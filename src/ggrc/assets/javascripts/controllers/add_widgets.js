/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: brad@reciprocitylabs.com
 * Maintained By: brad@reciprocitylabs.com
 */

//= require can.jquery-all

can.Control("CMS.Controllers.AddWidget", {
  defaults : {
      dashboard_controller : null
    , menu_tree : null
    , menu_view : GGRC.mustache_path + "/add_widget_menu.mustache"
    //, dropdown_view: '/static/mustache/add_widget_section.mustache'
  }
}, {

  init : function() {
    var that = this;

    can.view(this.options.menu_view, this.options.menu_tree, function(frag) {
      that.element
        .find(".dropdown-menu")
        .html(frag)
        .find(".divider:last").remove();
    });
  }

  , ".dropdown-menu > * click" : function(el, ev) {
    this.options.dashboard_controller
      .add_dashboard_widget_from_name(el.attr("class"))
  }

  /*, ".dropdown-toggle click" : function() {
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
  }*/
});
