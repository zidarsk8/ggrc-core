/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  can.Component.extend({
    tag: 'mapping-tree-view',
    template: can.view(GGRC.mustache_path +
      '/base_templates/mapping_tree_view.mustache'),
    scope: {
      reusable: '@',
      reuseMethod: '@',
      treeViewClass: '@',
      expandable: '@',
      parentInstance: null,
      mappedObjects: [],
      isExpandable: function () {
        var expandable = this.attr('expandable');
        if (expandable === null || expandable === undefined) {
          return true;
        } else if (typeof expandable === 'string') {
          return expandable === 'true';
        }
        return expandable;
      },
      refreshMappedObjects: function () {
        var binding;
        binding = this.parentInstance.get_binding(this.mapping);

        binding.refresh_instances().then(function (mappedObjects) {
          this.attr('mappedObjects').replace(mappedObjects);
        }.bind(this));
      }
    },
    init: function (element) {
      var $el = $(element);
      var scope = this.scope;
      var event = $el.data('event-type');
      var refreshMappedObjects = scope.refreshMappedObjects.bind(scope);
      _.each(['mapping', 'itemTemplate'], function (prop) {
        if (!scope.attr(prop)) {
          scope.attr(prop, $el.attr(can.camelCaseToDashCase(prop)));
        }
      }, this);
      $('body').on('update-mapping:' + event, refreshMappedObjects);

      refreshMappedObjects();
    },
    events: {
      '[data-toggle=unmap] click': function (el, ev) {
        var instance = el.find('.result').data('result');
        var scope = this.scope;
        var mappings = scope.parentInstance.get_mapping(scope.mapping);
        var binding;
        var refreshMappedObjects = scope.refreshMappedObjects.bind(scope);

        ev.stopPropagation();

        binding = _.find(mappings, function (mapping) {
          return mapping.instance.id === instance.id &&
            mapping.instance.type === instance.type;
        });
        _.each(binding.get_mappings(), function (mapping) {
          mapping.refresh()
            .then(function () {
              return mapping.destroy();
            })
            .then(refreshMappedObjects)
            .fail(function (err) {
              var messages = {
                '403': 'You don\'t have the permission to access the ' +
                'requested resource. It is either read-protected or not ' +
                'readable by the server.'
              };
              if (messages[err.status]) {
                $('body').trigger('ajax:flash',
                  {warning: messages[err.status]});
              }
            });
        });
      }
    }
  });
})(window.can, window.can.$);
