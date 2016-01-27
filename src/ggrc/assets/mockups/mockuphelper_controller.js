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
      new CMS.Controllers.MockupInfoPanel(this.element.find(".info-pin"), _.extend(options, {
        default_height: opts.infopin || "min"
      }));
      new CMS.Controllers.MockupModalView(this.element);

      this.element.find(".title-content").html(can.view(this.options.title_view, opts.object));
      this.options.views = views;
    },
    "{can.route} tab": function (router, ev, tab) {
      var exists = _.findWhere(this.options.views, {title: tab});
      if (!exists) {
        return can.route.attr("tab", _.first(this.options.views).title);
      }
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
      view: "/static/mustache/mockup_base_templates/nav_item.mustache"
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
      title_view: GGRC.mustache_path + "/title.mustache",
      slide_speed: 240
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
      },
      ".filter-trigger click": function (el, ev) {
        this.element.find(".filter-holder").slideToggle(this.options.slide_speed);
      },
      ".add-object-trigger click": function (el, ev) {
        ev.preventDefault();
        this.element.find('.new-relevant-block').last().clone().appendTo(".relevant-block-wrap");
      }
  });

  can.Control("CMS.Controllers.MockupModalView", {
  }, {
    ".modal .js-toggle-field change": function (el, ev) {
      var target = this.element.find(el.data("target")),
          val = el.data("value");

      target.prop("disabled", el.val() !== val);
    },
    ".modal #underAssessment change": function (el, ev) {
      var isEnabled = el.val() === "Control";
      this.element.find(".js-toggle-controlplans").prop("disabled", !isEnabled)
          .closest("label").toggleClass("disabled", !isEnabled);
    }
  });

})(this.can, this.can.$, GGRC.Mockup.Generator);
