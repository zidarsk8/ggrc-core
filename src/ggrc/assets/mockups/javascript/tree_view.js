/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $, Generator) {
   can.Control("CMS.Controllers.MockupTreeView", {
    }, {
    init: function (el, opts) {
      can.each(this.options.instance.children, function (child) {
        var $item = $("<li/>", {class: "tree-item"});
        new CMS.Controllers.MockupTreeItem($item, {
          item: child
        });
        this.element.append($item);
      }, this);
    },
    "{can.route} item": function (router, ev, item) {
      if (!item || !item.length) {
        return;
      }
      item = item.split("-");
      var view = _.findWhere(this.options.children, {
            type: item[0],
            id: item[1]
          });
      view.attr("active", true);
    },
    "{children} change": function (list, ev, which, type, status) {
      which = which.split(".");
      var index = +which[0],
          prop = which[1];

      if (!status) {
        return;
      }
      can.each(this.options.instance.children, function (child, i) {
        var isActive = index === i;
        child.attr("active", isActive);
        if (isActive) {
          can.route.attr("item", child.type + "-" + child.id);
        }
      });
    }
  });

  can.Control("CMS.Controllers.MockupTreeItem", {
    defaults: {
      view: "/static/mustache/mockup_base_templates/tree_item.mustache"
    }
  }, {
    init: function (el, options) {
      this.element.html(can.view(this.options.view, options.item));
      can.each(options.item.children, function (child) {
        var $item = $("<li/>", {class: "tree-item"});
        new CMS.Controllers.MockupTreeItem($item, {
          item: child
        });
        this.element.find(".tree-structure").append($item);
      }, this);
    },
    ".select click": function (el, ev) {
      var status = !this.options.item.active;
      this.options.item.attr("active", status);
    },
    "{item} change": function (list, ev, which, type, status) {
      if (which === "active") {
        this.element.toggleClass("active", status);
      }
    }
  });
})(this.can, this.can.$, GGRC.Mockup.Generator);

