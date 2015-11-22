/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function ($, CMS, GGRC) {
  /*
    WidgetList - an extensions-ready repository for widget descriptor configs.
    Create a new widget list with new GGRC.WidgetList(list_name, widget_descriptions)
      where widget_descriptions is an object with the structure:
      { <page_name> :
        { <widget_id> :
          { <widget descriptor-ready properties> },
        ...},
      ...}

    See the comments for GGRC.WidgetDescriptor for details in what is necessary to define
    a widget descriptor.
  */
  can.Construct("GGRC.WidgetList", {
    modules: {},
    /*
      get_widget_list_for: return a keyed object of widget descriptors for the specified page type.

      page_type - one of a GGRC object model's shortName, or "admin"

      The widget descriptors are built on the first call of this function; subsequently they are retrieved from the
       widget descriptor cache.
    */
    get_widget_list_for: function (page_type) {
      var widgets = {};
      can.each(this.modules, function (module) {
        can.each(module[page_type], function (descriptor, id) {
          if (!widgets[id]) {
            widgets[id] = descriptor;
          } else {
            can.extend(true, widgets[id], descriptor);
          }
        });
      });
      var descriptors = {};
      can.each(widgets, function (widget, widget_id) {
        switch (widget.content_controller) {
        case GGRC.Controllers.InfoWidget:
          descriptors[widget_id] = GGRC.WidgetDescriptor.make_info_widget(
            widget.content_controller_options && widget.content_controller_options.instance || widget.instance,
            widget.content_controller_options && widget.content_controller_options.widget_view || widget.widget_view
          );
          break;
        case GGRC.Controllers.TreeView:
          descriptors[widget_id] = GGRC.WidgetDescriptor.make_tree_view(
            widget.content_controller_options && (widget.content_controller_options.instance || widget.content_controller_options.parent_instance) || widget.instance,
            widget.content_controller_options && widget.content_controller_options.model || widget.far_model || widget.model,
            widget.content_controller_options && widget.content_controller_options.mapping || widget.mapping,
            widget
          );
          break;
        default:
          descriptors[widget_id] = new GGRC.WidgetDescriptor(page_type + ":" + widget_id, widget);
        }
      });
      can.each(descriptors, function (descriptor, id) {
        if (descriptor.suppressed) {
          delete descriptors[id];
        }
      });
      return descriptors;
    },
    /*
      returns a keyed object of widget descriptors that represents the current page.
    */
    get_current_page_widgets: function () {
      return this.get_widget_list_for(GGRC.page_instance().constructor.shortName);
    },
    get_default_widget_sort: function () {
      return this.sort;
    },
  }, {
    init: function (name, opts, sort) {
      this.constructor.modules[name] = this;
      can.extend(this, opts);
      if (sort && sort.length) {
        this.constructor.sort = sort;
      }
    },
    /*
      Here instead of using the object format described in the class comments, you may instead
      add widgets to the WidgetList by using add_widget.

      page_type - the shortName of a GGRC object class, or "admin"
      id - the desired widget's id.
      descriptor - a widget descriptor appropriate for the widget type. FIXME - the descriptor's
        widget_id value must match the value passed as "id"
    */
    add_widget: function (page_type, id, descriptor) {
      this[page_type] = this[page_type] || {};
      if (this[page_type][id]) {
        can.extend(true, this[page_type][id], descriptor);
      } else {
        this[page_type][id] = descriptor;
      }
    },
    suppress_widget: function (page_type, id) {
      this[page_type] = this[page_type] || {};
      if (this[page_type][id]) {
        can.extend(true, this[page_type][id], {
          suppressed: true
        });
      } else {
        this[page_type][id] = {
          suppressed: true
        };
      }
    }
  });
})(this.can.$, this.CMS, this.GGRC);
