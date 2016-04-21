/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function ($, CMS, GGRC) {
  //A widget descriptor has the minimum five properties:
  // widget_id:  the unique ID string for the widget
  // widget_name: the display title for the widget in the UI
  // widget_icon: the CSS class for the widget in the UI
  // content_controller: The controller class for the widget's content section
  // content_controller_options: options passed directly to the content controller; the
  //   precise options depend on the controller itself.  They usually require instance
  //   and/or model and some view.
  can.Construct("GGRC.WidgetDescriptor", {
    /*
      make an info widget descriptor for a GGRC object
      You must provide:
      instance - an instance that is a subclass of can.Model.Cacheable
      widget_view [optional] - a template for rendering the info.
    */
    make_info_widget: function (instance, widget_view) {
      var default_info_widget_view = GGRC.mustache_path + "/base_objects/info.mustache";
      return new this(
        instance.constructor.shortName + ":info", {
          widget_id: "info",
          widget_name: function () {
            if (instance.constructor.title_singular === 'Person')
              return 'Info';
            else
              return instance.constructor.title_singular + " Info";
          },
          widget_icon: "info-circle",
          content_controller: GGRC.Controllers.InfoWidget,
          content_controller_options: {
            instance: instance,
            model: instance.constructor,
            widget_view: widget_view || default_info_widget_view
          }
        });
    },
    /*
      make a tree view widget descriptor with mostly default-for-GGRC settings.
      You must provide:
      instance - an instance that is a subclass of can.Model.Cacheable
      far_model - a can.Model.Cacheable class
      mapping - a mapping object taken from the instance
      extenders [optional] - an array of objects that will extend the default widget config.
    */
    make_tree_view: function (instance, far_model, mapping, extenders) {
      var descriptor = {
        content_controller: CMS.Controllers.TreeView,
        content_controller_selector: "ul",
        widget_initial_content: '<ul class="tree-structure new-tree"></ul>',
        widget_id: far_model.table_singular,
        widget_guard: function () {
          if (far_model.title_plural === "Audits" && instance instanceof CMS.Models.Program) {
            return "context" in instance && !!(instance.context.id);
          }
          return true;
        },
        widget_name: function () {
          var $objectArea = $(".object-area");
          if ($objectArea.hasClass("dashboard-area") || instance.constructor.title_singular === "Person") {
            if (/dashboard/.test(window.location)) {
              return "My " + far_model.title_plural;
            } else {
              return far_model.title_plural;
            }
          } else if (far_model.title_plural === "Audits") {
            return "Mapped Audits";
          } else {
            return (far_model.title_plural === "References" ? "Linked " : "Mapped ") + far_model.title_plural;
          }
        },
        widget_icon: far_model.table_singular,
        object_category: far_model.category || 'default',
        model: far_model,
        content_controller_options: {
          child_options: [],
          draw_children: true,
          parent_instance: instance,
          model: far_model,
          list_loader: function () {
            return mapping.refresh_list();
          }
        }
      };

      $.extend.apply($, [true, descriptor].concat(extenders || []));

      return new this(instance.constructor.shortName + ":" + far_model.table_singular, descriptor);
    },
    newInstance: function (id, opts) {
      var ret;
      if (!opts && typeof id === "object") {
        opts = id;
        id = opts.widget_id;
      }

      if (GGRC.widget_descriptors[id]) {
        if (GGRC.widget_descriptors[id] instanceof this) {
          $.extend(GGRC.widget_descriptors[id], opts);
        } else {
          ret = this._super.apply(this);
          $.extend(ret, GGRC.widget_descriptors[id], opts);
          GGRC.widget_descriptors[id] = ret;
        }
        return GGRC.widget_descriptors[id];
      } else {
        ret = this._super.apply(this, arguments);
        $.extend(ret, opts);
        GGRC.widget_descriptors[id] = ret;
        return ret;
      }
    }
  }, {});
})(this.can.$, this.CMS, this.GGRC);
