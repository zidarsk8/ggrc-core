/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  if (!GGRC.tree_view) {
    GGRC.tree_view = new can.Map();
  }
  GGRC.tree_view.attr('basic_model_list', []);
  GGRC.tree_view.attr('sub_tree_for', {});

  can.Map.extend('CMS.Models.TreeViewOptions', {
    defaults: {
      instance: undefined,
      parent: null,
      children_drawn: false
    }
  }, {});

  can.Control.extend('CMS.Controllers.TreeLoader', {
    defaults: {}
  }, {
    init_spinner: function () {
      var renderer;
      var spinner;
      var $footer;
      var $wrapper;

      if (this.element) {
        $footer = this.element.children('.tree-item-add').first();

        if (this.options.is_subtree) {
          $wrapper = $('<li class="tree-item tree-spinner"/>');
        } else {
          $wrapper = $('<div class="tree-spinner"/>');
        }

        if (!this.options.is_subtree && !this.element.next().length) {
          $wrapper.css('height', '40px');
        }

        spinner = [
          '<spinner toggle="showMe"',
          '  size="large"',
          '  extra-css-class="tree-items"',
          '>',
          '</spinner>'
        ].join('');
        renderer = can.view.mustache(spinner);
        spinner = renderer({showMe: true});

        // Admin dashboard
        if ($footer.length === 0 &&
          this.element.children('.tree-structure').length > 0) {
          this.element.children('.tree-structure')
            .addClass('new-tree_loading').append($wrapper);
        } else if ($footer.length === 0) {  // My work
          this.element.addClass('new-tree_loading').append($wrapper);
        } else {
          $footer.before($wrapper);
        }

        $wrapper.append(spinner);
      }
    },
    prepare: function () {
      if (this._prepare_deferred) {
        return this._prepare_deferred;
      }

      this._prepare_deferred = can.Deferred();
      this._prepare_deferred.resolve();

      this._attached_deferred.then(function () {
        if (!this.element) {
          return;
        }
        can.trigger(this.element, 'updateCount', [0, this.options.update_count]);
        this.init_count();
      }.bind(this));

      return this._prepare_deferred;
    },

    show_info_pin: function () {
      var children;
      var controller;
      if (this.element && !this.element.data('no-pin')) {
        children = this.element.children();
        controller = children && children.find('.select:visible')
            .first()
            .closest('.cms_controllers_tree_view_node')
            .control();

        if (controller) {
          controller.select();
        }
      }
    },

    display: function (refetch) {
      var that = this;
      var tracker_stop = GGRC.Tracker.start(
        'TreeView', 'display', this.options.model.shortName);
      // TODO: Currently Query API doesn't support CustomAttributable.
      var isCustomAttr = /CustomAttr/.test(this.options.model.shortName);
      var isTreeView = this instanceof CMS.Controllers.TreeView;
      // Use Query API only for first tier in TreeViewController
      var loader = !isTreeView || isCustomAttr ||
      this.options.attr('is_subtree') ?
        this.fetch_list.bind(this) : this.loadPage.bind(this);

      if (this._display_deferred) {
        if (refetch) {
          return loader();
        }
        return this._display_deferred;
      }

      this._display_deferred = $.when(this._attached_deferred, this.prepare());

      this._display_deferred = this._display_deferred
        .then(this._ifNotRemoved(function () {
          return $.when(loader(), that.init_view());
        }))
        .then(that._ifNotRemoved(that.proxy('draw_list')))
        .done(tracker_stop);

      return this._display_deferred;
    },

    draw_list: function (list, is_reload, force_prepare_children) {
      is_reload = is_reload === true;
      // TODO figure out why this happens and fix the root of the problem
      if (!list && !this.options.list) {
        return undefined;
      }
      if (this._draw_list_deferred) {
        return this._draw_list_deferred;
      }
      this._draw_list_deferred = can.Deferred();
      if (this.element && !this.element.closest('body').length) {
        return undefined;
      }

      if (list) {
        list = list.length === null ? new can.List([list]) : list;
      } else {
        list = this.options.list;
      }

      if (!this.element) {
        return undefined;  // controller has been destroyed
      }

      this.options.attr('original_list', list);
      this.options.attr('list', []);
      this.on();

      this._draw_list_deferred =
        this.enqueue_items(list, is_reload, force_prepare_children);
      return this._draw_list_deferred;
    },

    _loading_started: function () {
      var $contentContainer;

      if (!this._loading_deferred) {
        this._loading_deferred = can.Deferred();

        // for some reason, .closest(<selector>) does not work, thus need to use
        // using a bit less roboust .parent()
        $contentContainer = this.element.parent();
        $contentContainer
          .find('spinner[extra-css-class="initial-spinner"]')
          .remove();

        this.init_spinner();  // the tree view's own items loading spinner
        this.element.trigger('loading');
      }
    },

    _loading_finished: function () {
      var loading_deferred;

      if (this._loading_deferred) {
        this.element.trigger('loaded');
        this.element.find('.tree-spinner').remove();

        if (this.element.hasClass('new-tree_loading')) {
          this.element.removeClass('new-tree_loading');
        } else {
          this.element.find('.new-tree_loading').removeClass('new-tree_loading');
        }

        loading_deferred = this._loading_deferred;
        this._loading_deferred = null;
        loading_deferred.resolve();
      }
    },

    enqueue_items: function (items, is_reload, force_prepare_children) {
      var child_tree_display_list = [];
      var filtered_items = [];
      var i;
      var refreshed_deferred;
      var that = this;
      var parent_model_name;
      var parent_instance_type;
      is_reload = is_reload === true;

      // find current widget model and check if first layer tree
      if (GGRC.page_object && this.options.parent) { // this is a second label tree
        parent_model_name = this.options.parent.options.model.shortName;
        parent_instance_type = this.options.parent.options.instance.type;
        child_tree_display_list =
          (GGRC.tree_view.sub_tree_for[parent_model_name] ||
            GGRC.tree_view.sub_tree_for[parent_instance_type] ||
            {} // all hope is lost, skip filtering
          ).display_list;

        // check if no objects selected, then skip filter
        if (!child_tree_display_list) {
          // skip filter
          filtered_items = items;
        } else if (child_tree_display_list.length === 0) { // no item is selected to filter, so just return
          return can.Deferred().resolve();
        } else {
          for (i = 0; i < items.length; i++) {
            if (child_tree_display_list.indexOf(items[i].instance.class.model_singular) !== -1) {
              filtered_items.push(items[i]);
            }
          }
        }
      } else {
        filtered_items = items;
      }

      if (!this._pending_items) {
        this._pending_items = [];
        this._loading_started();
      }

      if (!is_reload) {
        refreshed_deferred = $.when.apply($,
          can.map(filtered_items, function (item) {
            var instance = item.instance || item;
            if (instance.custom_attribute_values &&
              !GGRC.Utils.Snapshots.isSnapshot(instance)) {
              return instance.refresh_all('custom_attribute_values').then(function (values) {
                var rq = new RefreshQueue();
                _.each(values, function (value) {
                  if (value.attribute_object) {
                    rq.enqueue(value.attribute_object);
                  }
                });
                return rq.trigger().then(function () {
                  return values;
                });
              });
            }
          }));
      } else {
        refreshed_deferred = can.Deferred().resolve();
      }
      refreshed_deferred
        .then(function () {
          return that.insert_items(filtered_items, force_prepare_children);
        })
        .then(this._ifNotRemoved(this.proxy('_loading_finished')));

      return this._loading_deferred;
    },

    insert_items: function (items, force_prepare_children) {
      var that = this;
      var preppedItems = [];
      var idMap = {};
      var toInsert;
      var dfd;

      if (this.options.attr('is_subtree')) {
        // Check the list of items to be inserted for any duplicate items.
        can.each(this.options.list || [], function (item) {
          idMap[item.instance.type + item.instance.id] = true;
        });
        toInsert = _.filter(items, function (item) {
          return !idMap[item.instance.type + item.instance.id];
        });
      } else {
        toInsert = items;
      }

      can.each(toInsert, function (item) {
        var prepped = that.prepare_child_options(item, force_prepare_children);
        // Should we skip items without selfLink?
        if (prepped.instance.selfLink) {
          preppedItems.push(prepped);
        }
      });

      if (preppedItems.length > 0) {
        this.options.list.push.apply(this.options.list, preppedItems);
        dfd = this.add_child_lists(preppedItems);
      } else {
        dfd = can.Deferred().resolve();
      }

      return dfd;
    }
  });
})(window.can, window.$);
