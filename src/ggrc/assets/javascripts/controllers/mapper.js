/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  var selectors = ['unified-mapper', 'unified-search']
    .map(function (val) {
      return '[data-toggle="' + val + '"]';
    });
  var dataCorruptionMessage = 'Some Data is corrupted! ' +
              'Missing Scope Object';

  can.Control.extend('GGRC.Controllers.MapperModal', {
    defaults: {
      component: GGRC.mustache_path + '/modals/mapper/component.mustache'
    },
    launch: function ($trigger, options) {
      var href = $trigger.attr('data-href') || $trigger.attr('href');
      var modalId = 'ajax-modal-' + (href || '').replace(/[\/\?=\&#%]/g, '-').replace(/^-/, '');
      var $target = $('<div id="' + modalId + '" class="modal modal-selector hide"></div>');

      $target.modal_form({}, $trigger);
      this.newInstance($target[0], can.extend({
        $trigger: $trigger
      }, options));

      $target.on('hidden.bs.modal', function () {
        $(this).remove();
      });

      return $target;
    }
  }, {
    init: function () {
      this.element.html(can.view(this.options.component, this.options));
    }
  });

  $('body').on('click', selectors.join(', '), function (ev, disableMapper) {
    var relevantTo = null;
    var type;
    var btn = $(ev.currentTarget);
    var data = {};
    var joinType = btn.data('join-option-type');
    var isSearch;
    var snapshots = GGRC.Utils.Snapshots;
    var id = btn.data('join-object-id');
    var objectType = btn.data('join-object-type');
    var inScopeObject;

    can.each(btn.data(), function (val, key) {
      data[can.camelCaseToUnderscore(key)] = val;
    });

    if (data.tooltip) {
      data.tooltip.hide();
    }
    if (!data.clickable) {
      ev.preventDefault();
    }

    isSearch = /unified-search/ig.test(data.toggle);

    if (!disableMapper) {
      if (snapshots.isInScopeModel(objectType) && !isSearch) {
        /* if no id or object type is provided we shouldn't allow mapping */
        if (!id || !objectType) {
          return new Error('Required Data for In Scope Object is missing' +
            ' - Original Object is mandatory');
        }
        inScopeObject = CMS.Models[objectType].store[id];
        inScopeObject.updateScopeObject().then(function () {
          var scopeObject = inScopeObject.attr('scopeObject');
          if (!scopeObject.id) {
            GGRC.Errors.notifier('error', dataCorruptionMessage);
            setTimeout(function () {
              window.location.assign(location.origin + '/dashboard');
            }, 3000);
            return;
          }
          relevantTo = [{
            readOnly: true,
            type: scopeObject.type,
            id: scopeObject.id
          }];
          // Default Mapping Type should be Control
          type = joinType || 'Control';
          GGRC.Controllers.MapperModal.launch(btn, can.extend({
            object: objectType,
            'join-object-id': id,
            type: type,
            relevantTo: relevantTo
          }, data));
        });
      } else {
        type = joinType;
        GGRC.Controllers.MapperModal.launch(btn, can.extend({
          object: objectType,
          type: type,
          'join-object-id': id,
          'search-only': isSearch,
          template: {
            title: isSearch ?
              '/static/mustache/base_objects/modal/search_title.mustache' : ''
          }
        }, data));
      }
    }
  });
})(window.can, window.can.$);
