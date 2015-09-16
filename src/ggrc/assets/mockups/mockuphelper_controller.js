/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/


(function (can, $) {

  can.Control("CMS.Controllers.MockupHelper", {
    defaults: {
      title_view: GGRC.mustache_path + '/title.mustache',
      object_views: {},
    }
  }, {
    init: function (el, opts) {
      if (opts.object) {
        this.initObject(opts.object, el);
      }
      if (opts.views) {
        this.initViews(opts.views, el);
        this.options.object_views[opts.views[0].title].show();
      }
    },
    initObject: function (obj, el) {
      var content = el.find('.title-content');
      content.html(can.view(this.options.title_view, obj));
    },
    initViews: function (views, el) {
      var inner_content = $('.inner-content');
      _.forEach(views, function(view) {
        var placeholder = $("<div />"),
            v = new CMS.Controllers.MockupView(placeholder, view);
        inner_content.append(placeholder);
        this.options.object_views[view.title] = v;
      }.bind(this));
    },
    '.internav > li click': function(el, ev) {
      _.forEach(this.options.object_views, function(view) {
        view.element.hide();
      });
      var obj = el.find('a').attr('href').replace("#", "");
      el.siblings().removeClass('active')
      el.addClass('active');
      this.options.object_views[obj].element.show();
    }
  });

  can.Control("CMS.Controllers.MockupView", {
    defaults: {
      title_view: GGRC.mustache_path + '/title.mustache',
    }
  }, {
    init: function(el, opts) {
      this.initTab(opts);
      this.initContent(el, opts);
    },
    initTab: function(view) {
      var internav = $('.internav'),
          element = $("<li><a href='#" + view.title + "'></a></li>");
      element.find('a').html(can.view(this.options.title_view, view))
      internav.append(element);
      this.tab = element;
    },
    initContent: function(el, view) {
      this.element.html(can.view(GGRC.mustache_path + view.template, {instance: new can.Model.Cacheable(view), scope: view.scope}));
      _.forOwn(view.events, function(event_handler, event_name) {
        event_list = event_name.split(" ");
        event_name = event_list.pop();
        this.element.find(event_list.join(" ")).on(event_name, event_handler.bind(view));
      }.bind(this));
    },
    show: function() {
      this.element.siblings().hide();
      this.element.show();
      this.tab.siblings().removeClass('active');
      this.tab.addClass('active');
    }
  });
})(this.can, this.can.$);
