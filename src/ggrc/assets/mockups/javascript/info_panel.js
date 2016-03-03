/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $, Generator) {
  can.Control('CMS.Controllers.MockupInfoPanel', {
    defaults: {
      view: '/static/mustache/mockup_base_templates/info_panel.mustache',
      slide: 240,
      default_height: 'min',
      active_pin: null,
      minHeight: 240
    }
  }, {
    init: function () {
      this.options.active_pin = this.options.default_height;
      this.element.html(can.view(this.options.view, this.options));
      this.element.removeClass('hidden').height(0);
    },
    setSize: function (size) {
      var contentHeight;
      var height;
      function getHeight(height, size) {
        var increment = {
          deselect: 0,
          min: 1,
          normal: 2,
          max: 3
        };
        return increment[size] * height;
      }
      contentHeight = Math.floor(($(window).height() - $('.top-inner-nav').height() - $('.header-content').height() - $('.footer').height()) / 3) - 20;
      height = getHeight(contentHeight, size || this.options.default_height);

      this.element
        .show()
        .animate({
          height: height
        }, {
          duration: this.options.slide,
          complete: function () {
            if (size === 'deselect') {
              this.element.hide();
              this.active.attr('active', false);
              can.route.removeAttr('item');
            }
          }.bind(this)
        });
    },
    '.pin-action a click': function (el, ev) {
      var active = el.data('size');
      el.find('i').addClass('active').closest('li').siblings().find('i')
        .removeClass('active');
      this.options.active_pin = active;
      this.setSize(active);
    },
    '{can.route} tab': function (router, ev, tab) {
      this.activePanel = _.findWhere(this.options.views, {title: tab});
      this.element.height(0).hide();
    },
    '{can.route} item': function (router, ev, item) {
      var view;
      var tab;
      function findNeedle(list, slug) {
        var prop;
        var result;
        for (prop in list) {
          if (!list.hasOwnProperty(prop) || prop.indexOf('_') === 0) {
            continue;
          }
          if (list[prop].type === slug.type &&
              Number(list[prop].id) === Number(slug.id)) {
            return list[prop];
          }
          if (list[prop].children) {
            result = findNeedle(list[prop].children, slug);
            if (result) {
              return result;
            }
          }
        }
      }
      if (!item || !item.length) {
        return;
      }
      item = item.split('__');
      item = _.last(item).split('-');
      tab = _.filter(this.options.views, function (view) {
        return view.title === can.route.attr('tab');
      })[0];

      view = findNeedle(tab.children, {
        id: item[1],
        type: item[0]
      });

      if (this.cached) {
        this.cached.destroy();
      }
      this.cached = new CMS.Controllers.MockupInfoView(this.element.find('.tier-content'), {
        view: view
      });
      this.setSize();
    }
  });

  can.Control('CMS.Controllers.MockupInfoView', {
    defaults: {
      comment_attachments: new can.List(),
      templates: {
        assessment: '/static/mustache/mockup_base_templates/assessment_panel.mustache',
        task: '/static/mustache/mockup_base_templates/task_panel.mustache',
        'default': '/static/mustache/mockup_base_templates/request_panel.mustache'
      }
    }
  }, {
    init: function () {
      var template;
      if (!this.options.view || !this.options.view.type) {
        return;
      }
      template = this.options.templates[this.options.view.type] || this.options.templates.default;
      this.element.html(can.view(template, this.options.view));
    },
    '.js-trigger-reuse click': function (el, ev) {
      var view = this.options.view;
      var checked = _.reduce(this.options.view.past_requests, function (val, memo) {
        return val.concat(_.filter(memo.files, function (file) {
          var status = file.checked;
          file.attr('checked', false);
          return status;
        }));
      }, []);
      this.element.find('.past-items-list .js-trigger-pastfile')
        .prop('checked', false);
      view.comments.push({
        author: Generator.current.u,
        timestamp: Generator.current.d,
        attachments: checked,
        comment: ''
      });
    },
    '.js-trigger-pastfile change': function (el, ev) {
      var data = el.data('item');
      var isChecked = el.prop('checked');
      data.attr('checked', isChecked);
    }
  });
})(this.can, this.can.$, GGRC.Mockup.Generator);
