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
          new CMS.Controllers.MockupTreeView(this.element.find(".base-tree-view"), {
            instance: options.view
          });
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
      }
  });

  can.Control("CMS.Controllers.MockupModalView", {
    defaults: {
      instance: null
    }
  }, {
    '.modal hide': function (el, ev) {
      this.el = null;
      this.template = null;
      this.options.instance = null;
    },
    '.modal show': function (el, ev) {
      var template = el.data('template');
      var instance = el.data('instance');

      if (template) {
        this.options.originalInstance = instance.instance;
        this.options.instance = _.clone(instance.instance);
        this.template = can.view(template, _.extend(this.options.instance, {
          editable: true
        }));
        this.el = el;
        this.el.find('.modal-inner-content')
          .empty()
          .append(this.template);
      }
    },
    '.modal .add-task-trigger click': function (el, ev) {
      this.options.instance.tasks.push({
        type: 'task',
        title: {
          value: '',
          hidable: false
        },
        description: {
          value: '',
          hidable: true
        },
        task_type: {
          option: 'Rich text',
          value: '',
          hidable: true,
          size: 5
        },
        group: {
          value: '',
          hidable: true
        },
        start_date: {
          value: moment().format('MM/DD/YY'),
          hidable: false
        },
        end_date: {
          value: moment().format('MM/DD/YY'),
          hidable: false
        },
        mapped: {
          objects: {}
        }
      });
      if (this.options.instance.tasks.length > 1) {
        $(".modal .close-block").removeClass("hidden");
      }
    },
    ".modal .close-trigger click": function (el, ev) {
      var repeatBlock,
          close = $(".modal .close-block");

      el.closest('.repeated-block').remove();
      repeatBlock = $('.modal .repeated-block').length;

      if (repeatBlock === 1) {
        close.addClass("hidden");
      }
    },
    ".modal .js-toggle-field change": function (el, ev) {
      var target = this.element.find(el.data("target")),
          val = el.data("value");

      target.prop("disabled", el.val() !== val);
    },
    ".modal #underAssessment change": function (el, ev) {
      var isEnabled = el.val() === "Control";
      this.element.find(".js-toggle-controlplans").prop("disabled", !isEnabled)
          .closest("label").toggleClass("disabled", !isEnabled);
    },
    ".modal .task-people-trigger change": function (el, ev) {
      var isEach = el.val() === 'each',
          isAll = el.val() === 'all';

      if (isEach) {
        this.element.find('.people-option').show();
        this.element.find('.people-regular').hide();
        this.element.find('.active-trigger').addClass('disabled');
        this.element.find('.active-trigger').attr('rel', 'tooltip');
        this.element.find('.active-trigger')
        .attr('data-original-title', 'Save draft and go to Setup workflow to activate it');
      } else if (isAll) {
        this.element.find('.people-option').hide();
        this.element.find('.people-regular').show();
        this.element.find('.active-trigger').removeClass('disabled');
        this.element.find('.active-trigger').removeAttr('rel');
        this.element.find('.active-trigger').removeAttr('data-original-title');
      }
    },
    '.all change' : function (el, ev) {
      var $allTrigger = $('.all'),
          $allCheckboxes = $('.attr-checkbox'),
          $hidable = $('.hidable');

      if (!$allTrigger.hasClass('triggered')) {
        $allTrigger.addClass('triggered');
        $hidable.removeClass('hidden');
        $allCheckboxes.prop('checked', true);
      } else {
        $allTrigger.removeClass('triggered');
        $hidable.addClass('hidden');
        $allCheckboxes.prop('checked', false);
      }
    },
    ".type-select change": function (el, ev) {
      var isOptions = el.val() === 'menu' || el.val() === 'checkbox',
          isText = el.val() === 'text';

      if (isOptions) {
        this.element.find('.text-wrap').hide();
        this.element.find('.options-wrap').show();
      } else if (isText) {
        this.element.find('.text-wrap').show();
        this.element.find('.options-wrap').hide();
      }
    },
    "a.field-hide click" : function(el, ev) { //field hide
      var $el = $(el),
        $hidable = $el.closest('[class*="span"].hidable');

      $hidable.addClass("hidden");
      this.options.reset_visible = true;
      var ui_unit = $hidable.find('[tabindex]');
      var i, tab_value;
      for (i = 0; i < ui_unit.length; i++) {
        tab_value = $(ui_unit[i]).attr('tabindex');
        if(tab_value > 0) {
          this.options.ui_array[tab_value-1] = 1;
          $(ui_unit[i]).attr('tabindex', '-1');
          $(ui_unit[i]).attr('uiindex', tab_value);
        }
      }
      return false;
    },
    '.dropdown-menu-form ul click' : function (el, ev) {
      ev.stopPropagation();
    },
    '.dropdown-menu-form input change' : function (el, ev) {
      var checkedValue = el.val(),
          targetValue = this.element
          .find("[data-value='" + checkedValue + "']");

      if (targetValue.hasClass('hidden')) {
        targetValue.removeClass('hidden');
      } else {
        targetValue.addClass('hidden');
      }
    },
    ".object-check-all click": function (el, ev) {
      ev.preventDefault();

      this.element.find('.object-check-single').prop('checked', true);
    }
  });

})(this.can, this.can.$, GGRC.Mockup.Generator);
