/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (GGRC, can, $) {
  can.Component.extend({
    tag: 'tabs',
    template: can.view(GGRC.mustache_path + '/base_objects/tabs.mustache'),
    scope: {
      panels: [],
      index: 0,
      /**
       * Activate currently clicked panel
       *
       * @param {Object} scope - current item value from `scope.panels`
       * @param {jQuery.Object} el - clicked element
       * @param {Object} ev - click event handler
       */
      setActive: function (scope, el, ev) {
        ev.preventDefault();
        scope.panel.attr('active', true);
        this.attr('index', Number(el.data('index')));
      }
    },
    events: {
      /**
       * Set default active tab if none defined
       *
       * @param {can.List} list - list of items in `panels` object
       * @param {Object} ev - event triggered on change length
       * @param {String} item - item that got changed
       * @param {String} action - in our case it can be `add` or `remove`
       */
      '{scope.panels} change': _.throttle(function (list, ev, item, action) {
        var panels = this.element.find('tab-panel');
        var index = this.scope.attr('index');
        var active;

        if (list.length !== panels.length) {
          return;
        }
        active = _.filter(list, function (item) {
          if (item.panel) {
            return item.panel.attr('active');
          }
        });
        if (!active.length) {
          list[index].panel.attr('active', true);
        }
      }, 10)
    }
  });

  GGRC.Components("tabPanel", {
    tag: 'tab-panel',
    template: can.view(GGRC.mustache_path + '/base_objects/tab_panel.mustache'),
    scope: {
      active: false,
      title: '@',
      panels: null
    },
    events: {
      /**
       * Add this `panel` to `panels` list in fomat
       * {
       *   title: `Title`
       *   panel: `Current panel scope`
       * }
       */
      inserted: function () {
        var panels = this.scope.attr('panels');
        panels.push({
          title: this.scope.attr('title'),
          panel: this.scope
        });
      },
      /**
       * Check if other tabs are active and deactivate them
       *
       * @param {can.List} list - list of items in `panels` object
       * @param {Object} ev - event triggered on change
       * @param {String} item - item that got changed
       * @param {String} action - what got changed on the object
       * @param {String} status - status of changed item, we are looking for `active`
       *                          property change to either `true` or `false`
       */
      '{scope.panels} change': function (list, ev, item, action, status) {
        var index;
        var panel;

        item = item.split('.');
        if (item.length !== 3 || item[1] !== "panel" || item[2] !== "active") {
          // if this is a change to a scope in a different panel we should
          // not switch tabs
          return;
        }
        index = Number(item[0]);
        panel = list[index].panel;
        if (status && this.scope !== panel) {
          this.scope.attr('active', false);
        }
      }
    }
  });
})(window.GGRC, window.can, window.can.$);
