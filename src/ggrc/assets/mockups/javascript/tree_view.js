/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $, Generator) {
  can.Control('CMS.Controllers.MockupTreeView', {
  }, {
    init: function (el, opts) {
      can.each(this.options.instance.children, function (child) {
        var $item = $('<li/>', {'class': 'tree-item'});
        new CMS.Controllers.MockupTreeItem($item, {
          item: child
        });
        this.element.append($item);
      }, this);
    },
    '{can.route} item': function (router, ev, current, previous) {
      if (!previous) {
        return;
      }
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
      current = current.split('__');
      previous = previous.split('__');
      _.each(_.difference(previous, current), function (slug) {
        var item;
        slug = slug.split('-');
        item = findNeedle(this.options.instance.children, {
          id: slug[1],
          type: slug[0]
        });
        if (item) {
          item.attr('active', false);
        }
      }, this);
    },
    '{instance.children} change': function (list, ev, which, type, status) {
      var groups = groupChanged(which.split('.'));
      var instance = this.options.instance;
      var url = [];
      function groupChanged(arr) {
        var groups = [];
        var check = arr;
        while (check.length) {
          check = arr.splice(0, 2);
          if (check.length) {
            groups.push(check);
          }
        }
        return groups;
      }
      if (!status) {
        return;
      }

      can.each(groups, function (group) {
        var index = Number(group[0]);
        var prop = group[1];

        if (prop === 'active') {
          instance = instance.children[index];

          url.push(instance.type + '-' + instance.id);
          instance.attr('active', true);
          can.route.attr('item', url.join('__'));
        } else {
          instance = instance[prop][index];
          url.push(instance.type + '-' + instance.id);
          instance.attr('active', true);
        }
      }, this);
    }
  });

  can.Control('CMS.Controllers.MockupTreeItem', {
    defaults: {
      templates: {
        task: '/static/mustache/mockup_base_templates/tree_item_task.mustache',
        task_group: '/static/mustache/mockup_base_templates/tree_item_task.mustache',
        workflow: '/static/mustache/mockup_base_templates/tree_item_task.mustache',
        'default': '/static/mustache/mockup_base_templates/tree_item.mustache'
      }
    }
  }, {
    init: function (el, options) {
      var template = this.options.templates[options.item.type] ||
        this.options.templates.default;

      this.element.html(can.view(template, options.item));
      can.each(options.item.children, function (child) {
        var $item = $('<li/>', {'class': 'tree-item'});
        new CMS.Controllers.MockupTreeItem($item, {
          item: child
        });
        this.element.find('.tree-structure').append($item);
      }, this);
    },
    '.select click': function (el, ev) {
      var item = el.closest('.tree-item');
      var status = this.options.item.attr('active');
      if (this.element.is(item)) {
        if (status) {
          this.options.item.attr('active', false);
        }
        this.options.item.attr('active', true);
      }
    }
  });
})(this.can, this.can.$, GGRC.Mockup.Generator);

