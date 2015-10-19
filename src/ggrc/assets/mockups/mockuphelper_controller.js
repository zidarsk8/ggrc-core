/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/


(function (can, $, Generator) {
  can.route(":tab", {tab: "Info"});
  can.route(":tab/:item");

  // Activate router
  $(document).ready(can.route.ready);

  can.Control("CMS.Controllers.MockupHelper", {
    defaults: {
      title_view: GGRC.mustache_path + "/title.mustache",
      object_views: {},
      cached: null
    }
  }, {
    init: function (el, opts) {
      var views = new can.Map(_.map(opts.views, function (view) {
            return new can.Model.Cacheable(view);
          })),
          options = {
            views: views
          };
      new CMS.Controllers.MockupNav(this.element.find(".internav"), options);
      new CMS.Controllers.MockupInfoPanel(this.element.find(".info-pin"), options);
      new CMS.Controllers.MockupModalView(this.element);

      this.element.find(".title-content").html(can.view(this.options.title_view, opts.object));
      this.options.views = views;
    },
    "{can.route} tab": function (router, ev, tab) {
      this.options.views.each(function (view) {
        var isActive = view.title === tab;
        view.attr("active", isActive);
        if (isActive) {
          if (this.cached) {
            this.cached.destroy();
          }
          this.cached = new CMS.Controllers.MockupView(this.element.find(".inner-content"), {
            view: view
          });
        }
      }.bind(this));
    }
  });

  can.Control("CMS.Controllers.MockupNav", {
    defaults: {
      view: "/static/mockups/base_templates/nav_item.mustache"
    }
  }, {
    "{views} change": function (list, ev, which, type, status) {
      which = which.split(".");
      var index = +which[0],
          prop = which[1];
      if (prop === "active" && status) {
        this.element.html(can.view(this.options.view, this.options));
      }
    }
  });

  can.Control("CMS.Controllers.MockupView", {
    defaults: {
      title_view: GGRC.mustache_path + "/title.mustache"
    }
  }, {
      init: function (el, options) {
        this.element.html(can.view(GGRC.mustache_path + options.view.template, _.extend(this.options, {
          instance: options.view
        })));
        if (options.view.children) {
          new CMS.Controllers.MockupTreeView(this.element.find(".base-tree-view"), options.view);
        }
        if (options.view.title === "Info") {
          this.cached = new CMS.Controllers.MockupInfoView(this.element);
        }
      },
      destroy: function () {
        if (this.cached) {
          this.cached.destroy();
        }
        can.Control.prototype.destroy.call(this);
      }
  });

  can.Control("CMS.Controllers.MockupInfoView", {
    defaults: {
      comment_attachments: new can.List()
    }
  }, {
    ".js-trigger-reuse click": function (el, ev) {
      var view = this.options.view,
          checked = _.reduce(this.options.view.past_requests, function (val, memo) {
            return val.concat(_.filter(memo.files, function (file) {
              var status = file.checked;
              file.attr("checked", false);
              return status;
            }));
          }, []);
      this.element.find(".past-items-list .js-trigger-pastfile").prop("checked", false);
      view.comments.push({
        author: Generator.current.u,
        timestamp: Generator.current.d,
        attachments: checked,
        comment: ""
      });
    },
    ".js-trigger-pastfile change": function (el, ev) {
      var data = el.data("item"),
          isChecked = el.prop("checked");
      data.attr("checked", isChecked);
    },
    ".show-hidden-fields click": function (el, ev) {
      $(".hidden-fields-area").toggleClass("active");
    }
  });

  can.Control("CMS.Controllers.MockupModalView", {
  }, {
    ".modal #assessorDefault change": function (el, ev) {
      this.element.find(".js-toggle-chooseperson").prop("disabled", el.val() !== "other");
    },
    ".modal #underAssessment change": function (el, ev) {
      var isEnabled = el.val() === "Control";
      this.element.find(".js-toggle-controlplans").prop("disabled", !isEnabled)
          .closest("label").toggleClass("disabled", !isEnabled);
    }
  });

  can.Control("CMS.Controllers.MockupTreeView", {
  }, {
    init: function (el, opts) {
      _.each(this.options.children, function (child) {
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
      _.each(this.options.children, function (child, i) {
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
      view: "/static/mockups/base_templates/tree_item.mustache"
    }
  }, {
    init: function (el, options) {
      this.element.html(can.view(this.options.view, options.item));
      _.each(options.item.children, function (child) {
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


  can.Control("CMS.Controllers.MockupInfoPanel", {
    defaults: {
      view: "/static/mockups/base_templates/info_panel.mustache",
      slide: 240,
      minHeight: 240
    }
  }, {
    "setSize": function (size) {
      function get_height(height, size) {
         var increment = {
          deselect: 0,
          min: 1,
          normal: 2,
          max: 3
        };
        return increment[size] * height;
      }
      var height = get_height(Math.floor($(".content").height()/3), size || "min");
      this.element
        .show()
        .removeClass("hidden")
        .animate({
          height: height
        }, {
          duration: this.options.slide,
          complete: function () {
            if (size === "deselect") {
              this.element.hide();
              this.active.attr("active", false);
              can.route.removeAttr("item");
            }
          }.bind(this)
        });
    },
    ".pin-action a click": function (el, ev) {
      el.find("i").css("opacity", 1).closest("li").siblings().find("i").css("opacity", 0.25);
      this.setSize(el.data("size"));
    },
    "{can.route} tab": function (router, ev, tab) {
      this.activePanel = _.findWhere(this.options.views, {title: tab});
      this.element.hide();
    },
    "{can.route} item": function (router, ev, item) {
      // TODO: Simplify this
      if (!item || !item.length) {
        return;
      }
      function recursiveFind(needle) {
        if (needle.type === item[0] && needle.id === item[1]) {
          return needle;
        }
        if (needle.children && needle.children.length) {
          return _.map(needle.children, recursiveFind);
        }
      }
      item = item.split("-");
      var view = _.compact(_.flattenDeep(_.map(this.options.views, recursiveFind)))[0];
      this.active = view;
      this.element.html(can.view(this.options.view, view));
      if (this.cached) {
        this.cached.destroy();
      }
      this.cached = new CMS.Controllers.MockupInfoView(this.element.find(".tier-content"), {
        view: view
      });
      this.setSize();
    }
  });

  can.Component.extend({
    tag: "attachment-list",
    template: can.view("/static/mockups/base_templates/attachment_list.mustache"),
    scope: {
      title: "@",
      types: "@",
      files: new can.List()
    },
    events: {
      "inserted": "updateFiles",
      "{scope.data} add": "updateFiles",
      "{scope.data} remove": "updateFiles",
      "updateFiles": function () {
        var types = this.scope.attr("types"),
            isNegation = types.charAt(0) === "!",
            result;
        if (isNegation) {
          types = types.slice(1);
        }
        result = _.reduce(this.scope.attr("data"), function (memo, comment) {
          var attachments = _.filter(comment.attachments, function (attachment) {
            if (isNegation) {
              return attachment.extension !== types;
            }
            return attachment.extension === types;
          });
          if (attachments.length) {
            return memo.concat(attachments);
          }
          return memo;
        }, []);
        this.scope.attr("files", result);
      }
    }
  });
  can.Component.extend({
    tag: "add-comment",
    template: can.view("/static/mockups/base_templates/add_comment.mustache"),
    scope: {
      attachments: new can.List()
    },
    events: {
      "cleanPanel": function () {
        this.scope.attachments.replace([]);
        this.element.find("textarea").val("");
      },
      ".js-trigger-attachdata click": function (el, ev) {
        var type = el.data("type"),
            typeFn = Generator[type];
        if (!typeFn) {
          return;
        };
        this.scope.attachments.push(typeFn());
      },
      ".btn-success click": function (el, ev) {
        var $textarea = this.element.find(".add-comment textarea"),
            text = $.trim($textarea.val()),
            attachments = this.scope.attachments;

        if (!text.length && !attachments.length) {
          return;
        }
        this.scope.data.unshift({
          author: Generator.current.u,
          timestamp: Generator.current.d,
          comment: text,
          attachments: _.map(attachments, function (attachment) {
            return attachment;
          })
        });
        this.cleanPanel();
      }
    }
  });
})(this.can, this.can.$, GGRC.Mockup.Generator);
