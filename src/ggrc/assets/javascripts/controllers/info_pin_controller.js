/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

can.Control('CMS.Controllers.InfoPin', {
  defaults: {
    view: GGRC.mustache_path + '/base_objects/info.mustache'
  }
}, {
  init: function (el, options) {
    this.element.height(0);
  },
  findView: function (instance) {
    var view = instance.class.table_plural + '/info';

    if (instance instanceof CMS.Models.Person) {
      view = GGRC.mustache_path +
        '/ggrc_basic_permissions/people_roles/info.mustache';
    } else if (view in GGRC.Templates) {
      view = GGRC.mustache_path + '/' + view + '.mustache';
    } else {
      view = this.options.view;
    }
    if (instance.info_pane_preload) {
      instance.info_pane_preload();
    }
    return view;
  },
  findOptions: function (el) {
    var treeNode = el.closest('.cms_controllers_tree_view_node').control();
    return treeNode.options;
  },
  loadChildTrees: function () {
    var childTreeDfds = [];
    var that = this;
    var $el;
    var childTreeControl;

    this.element.find('.' + CMS.Controllers.TreeView._fullName)
      .each(function (_, el) {
        $el = $(el);

        //  Ensure this targets only direct child trees, not sub-tree trees
        if ($el.closest('.' + that.constructor._fullName).is(that.element)) {
          childTreeControl = $el.control();
          if (childTreeControl)
            childTreeDfds.push(childTreeControl.display());
        }
      });
  },
  hideInstance: function () {
    this.element.stop(true);
    this.element.height(0).html('');
    $(window).trigger('resize');
  },
  unsetInstance: function () {
    this.element.stop(true);
    this.element.animate({
      height: 0
    }, {
      duation: 800,
      complete: function () {
        this.element.html('');
        $('.cms_controllers_tree_view_node').removeClass('active');
        $(window).trigger('resize');
      }.bind(this)
    });
  },
  setInstance: function (instance, el) {
    var options = this.findOptions(el);
    var view = this.findView(instance);
    var panelHeight = $(window).height() / 3;
    var confirmEdit = instance.class.confirmEditModal ?
      instance.class.confirmEditModal : {};

    if (!_.isEmpty(confirmEdit)) {
      confirmEdit.confirm = this.confirmEdit;
    }

    this.element.html(can.view(view, {
      instance: instance,
      model: instance.class,
      confirmEdit: confirmEdit,
      is_info_pin: true,
      options: options,
      result: options.result,
      page_instance: GGRC.page_instance()
    }));

    // Load trees inside info pin
    this.loadChildTrees();

    // Make sure pin is visible
    if (!this.element.height()) {
      this.element.animate({
        height: panelHeight
      }, {
        duration: 800,
        easing: 'easeOutExpo',
        complete: function () {
          this.ensureElementVisible(el);
        }.bind(this)
      });
    } else {
      this.ensureElementVisible(el);
    }
  },
  ensureElementVisible: function (el) {
    var $objectArea;
    var $header;
    var $filter;
    var elTop;
    var elBottom;
    var headerTop;
    var headerBottom;
    var infoTop;

    $(window).trigger('resize');
    $objectArea = $('.object-area');
    $header = $('.tree-header:visible');
    $filter = $('.tree-filter:visible');

    elTop = el.offset().top;
    elBottom = elTop + el.height();

    headerTop = $header.offset().top;
    headerBottom = headerTop + $header.height();
    infoTop = this.element.offset().top;

    if (elTop < headerBottom || elBottom > infoTop) {
      el[0].scrollIntoView(false);
      if (elTop < headerBottom) {
        el[0].scrollIntoView(true);
        $objectArea.scrollTop(
          $objectArea.scrollTop() - $header.height() - $filter.height());
      } else {
        el[0].scrollIntoView(false);
      }
    }
  },
  confirmEdit: function (instance, modalDetails) {
    var confirmDfd = $.Deferred();
    var renderer = can.view.mustache(modalDetails.description);
    GGRC.Controllers.Modals.confirm({
      modal_description: renderer(instance).textContent,
      modal_confirm: modalDetails.button,
      modal_title: modalDetails.title,
      button_view: GGRC.mustache_path + '/quick_form/confirm_buttons.mustache'
    }, confirmDfd.resolve);
    return confirmDfd;
  },
  '.pin-action a click': function (el) {
    var $win = $(window);
    var winHeight = $win.height();
    var options = {
      duration: 800,
      easing: 'easeOutExpo'
    };
    var targetHeight = {
      min: 75,
      normal: (winHeight / 3),
      max: (winHeight * 3 / 4)
    };
    var $info = this.element.find('.info');
    var type = el.data('size');
    var size = targetHeight[type];

    if (type === 'deselect') {
      // TODO: Make some direct communication between the components
      //       and make sure only one widget has 'widget-active' class
      el.find('[rel=tooltip]').data('tooltip').hide();
      $('.widget-area .widget:visible').find('.cms_controllers_tree_view')
        .control().deselect();
      this.unsetInstance();
      return;
    }
    this.element.find('.pin-action i').css({opacity: 0.25});

    if (size < $info.height()) {
      options.start = function () {
        $win.trigger('resize', size);
      };
    } else {
      options.complete = function () {
        $win.trigger('resize');
      };
    }

    this.element.animate({height: size}, options);
    el.find('i').css({opacity: 1});
  }
});
