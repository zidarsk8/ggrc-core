/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/


(function (can, $) {
  can.route(":tab", {tab: "Info"});
  can.route(":tab/:id");

  // Activate router
  $(document).ready(can.route.ready);

  can.Control("CMS.Controllers.MockupHelper", {
    defaults: {
      title_view: GGRC.mustache_path + "/title.mustache",
      object_views: {}
    }
  }, {
    init: function (el, opts) {
      var options = {
        views: this.options.views
      };
      new CMS.Controllers.MockupNav(this.element.find(".internav"), options);
      new CMS.Controllers.MockupView(this.element.find(".inner-content"), options);
      this.element.find(".title-content").html(can.view(this.options.title_view, opts.object));
    },
    "{can.route} tab": function (router, ev, tab) {
      _.each(this.options.views, function (view) {
        view.active = view.title === tab;
      });
    }
  });

  can.Control("CMS.Controllers.MockupNav", {
    defaults: {
      view: "/static/mockups/base_templates/nav_item.mustache"
    }
  }, {
    "{can.route} tab": function () {
      this.element.html(can.view(this.options.view, this.options));
    }
  });

  can.Control("CMS.Controllers.MockupView", {
    defaults: {
      title_view: GGRC.mustache_path + "/title.mustache"
    }
  }, {
    "{can.route} tab": function () {
      var view = _.findWhere(this.options.views, {active: true});
      this.element.html(can.view(GGRC.mustache_path + view.template, {
        instance: new can.Model.Cacheable(view),
        scope: view.scope
      }));
    }
  });

  can.Control("CMS.Controllers.MockupTreeView", {
  }, {
    init: function (el, opts) {
    }
  });
})(this.can, this.can.$);
