/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/


can.Control("CMS.Controllers.InfoPane", {
  defaults: {
    view: GGRC.mustache_path + "/base_objects/info.mustache"
  }
}, {
  init: function(el, options) {
    var instance = GGRC.page_instance();
    this.element.height(0);
  },
  findView: function(instance) {
    var view = instance.class.table_plural + "/info";

    if (instance instanceof CMS.Models.Person) {
      view = GGRC.mustache_path + "/ggrc_basic_permissions/people_roles/info.mustache";
    } else if (view in GGRC.Templates) {
      view = GGRC.mustache_path + "/" + view + ".mustache";
    } else {
      view = this.options.view;
    }
    return view;
  },
  findTreeController: function(el) {
    return el.closest('.cms_controllers_tree_view').control();
  },
  findResult: function(el) {
    var tree_node = el.closest('.cms_controllers_tree_view_node'),
        tree_controller = this.findTreeController(el),
        result;

    can.each(tree_controller.options.original_list, function(item) {
      var id = tree_node.data('object-id');
      if (id && item.instance && item.instance.id === id) {
        result = item;
      }
    });
    return result;
  },
  setInstance: function(instance, el) {
    if (!instance) {
      this.element.html('');
      this.element.height(0);
      $('.cms_controllers_tree_view_node').removeClass('active');
      return;
    }
    var result = this.findResult(el),
        view = this.findView(instance),
        options = this.findTreeController(el).options;
    this.element.html(can.view(view, {
      instance: instance,
      model: instance.class,
      result: result,
      mappings: result.mappings_compute(),
      is_info_pane: true,
      options: options
    }));
    var height = $(window).height(),options = {
        duration: 800,
        easing: 'easeOutExpo'
    };
    if (!this.element.height()) {
      this.element.animate({ height: height / 3 }, options);
    }
  },
  '.pin-action a click': function(el) {
    var options = {
        duration: 800,
        easing: 'easeOutExpo'
      },
      $info = this.element.find('.info'),
      height = $(window).height();
    this.element.find('.pin-action i').css({'opacity': 0.25});
    if (el.hasClass('min')) {
      this.element.animate({height: 75}, options);
      el.find('i').css({'opacity':1});
    } else if (el.hasClass('max')) {
      this.element.animate({ height: height * 3 / 4 }, options);
      el.find('i').css({'opacity':1});
    } else {
      this.element.animate({height: height / 3}, options);
      el.find('i').css({'opacity':1});
    }
  }
});
