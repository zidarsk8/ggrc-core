/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  can.Component.extend({
    tag: 'tabs',
    template: can.view(GGRC.mustache_path + '/base_objects/tabs.mustache'),
    scope: {
      panels: [],
      setActive: function (scope, el, ev) {
        ev.preventDefault();
        scope.panel.attr('active', true);
      }
    },
    events: {
      '{scope.panels} length': function (list, ev, item, action, status) {
        var panels = this.element.find('tab-panel');
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
          list[0].panel.attr('active', true);
        }
      }
    }
  });

  can.Component.extend({
    tag: 'tab-panel',
    template: can.view(GGRC.mustache_path + '/base_objects/tab_panel.mustache'),
    scope: {
      active: false,
      title: '@',
      panels: null
    },
    events: {
      inserted: function () {
        var panels = this.scope.attr('panels');
        panels.push({
          title: this.scope.attr('title'),
          panel: this.scope
        });
      },
      '{scope.panels} change': function (list, ev, item, action, status) {
        var index;
        var panel;

        item.split('.');
        index = Number(item[0]);
        panel = list[index].panel;
        if (status && this.scope !== panel) {
          this.scope.attr('active', false);
        }
      }
    }
  });
})(window.can, window.can.$);
