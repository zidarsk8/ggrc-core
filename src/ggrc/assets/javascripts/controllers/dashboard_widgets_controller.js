/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all
//= require controllers/filterable_controller

CMS.Controllers.Filterable("CMS.Controllers.DashboardWidgets", {
  defaults : {
    model : null
    , widget_id : ""
    , widget_name : ""
    , widget_icon : ""
    , widget_view : "/static/mustache/dashboard/object_widget.mustache"
    , show_filter : false
    , object_category : null //e.g. "governance"
    , content_selector : ".content"
    , minimum_widget_height : 100
    , content_controller : null
    , content_controller_options : {}
  }
}, {

  init : function() {

    if(!this.options.model && GGRC.page_model) {
      this.options.model = GGRC.infer_object_type(GGRC.page_model);
    }

    if(!this.options.widget_icon && this.options.model) {
      this.options.widget_icon = this.options.model.table_singular;
    }

    if(!this.options.object_category && this.options.model) {
      this.options.object_category = this.options.model.category;
    }

    this.element
    .addClass("widget")
    .addClass(this.options.object_category)
    .attr("id", this.options.widget_id + "_widget")
    .css("height", this.options.minimum_widget_height)
    .html($(new Spinner().spin().el).css({
        width: '100px',
        height: '100px',
        left: '50px',
        top: '50px'
        }))
    .trigger("section_created");

    $.when(
      can.view(this.options.widget_view, $.when(this.options))
      , CMS.Models.DisplayPrefs.findAll()
    ).done(this.proxy("draw_widget"));
  }

  , draw_widget : function(frag, prefs) {

    this.element.html(frag);

    var content = this.element;
    if(prefs[0].getCollapsed(window.getPageToken(), this.element.attr("id"))) {

      this.element
      .find(".widget-showhide > a")
      .showhide("hide");

      content.add(this.element).css("height", "");
      if(content.is(".ui-resizable")) {
        content.resizable("destroy");
      }
    } else {
      content.trigger("min_size");
    }

      // this.element
      // .find('.wysihtml5')
      // .cms_wysihtml5();
    if(this.options.content_controller) {
      this.element
      .find(this.options.content_selector)
      .html($(new Spinner().spin().el).css({
        width: '100px',
        height: '100px',
        left: '50px',
        top: '50px'
        }));
      new this.options.content_controller(
        this.element.find(this.options.content_selector)
        , this.options.content_controller_options
      );
    }

  }

  , ".remove-widget click" : function() {
    var parent = this.element.parent();
    this.element.remove();
    parent.trigger("sortremove");
  }

  , ".widgetsearch keydown" : function(el, ev) {
    if(ev.which === 13) {
      this.filter(el.val());
      this.element.trigger('kill-all-popovers');
    }
    ev.stopPropagation();
    ev.originalEvent && ev.originalEvent.stopPropagation();
  }

  , " updateCount" : function(el, ev, count) {
    this.element.find(".header .object_count").html(count);
  }
});
