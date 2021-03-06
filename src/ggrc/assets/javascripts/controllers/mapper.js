/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  var selectors = _.map(['unified-mapper', 'unified-search'], function (val) {
    return '[data-toggle="' + val + '"]';
  });

  can.Control('GGRC.Controllers.MapperModal', {
    defaults: {
      component: GGRC.mustache_path + '/modals/mapper/component.mustache'
    },
    launch: function ($trigger, options) {
      var href = $trigger.attr('data-href') || $trigger.attr('href');
      var modalId = 'ajax-modal-' + (href || '').replace(/[\/\?=\&#%]/g, '-').replace(/^-/, '');
      var $target = $('<div id="' + modalId + '" class="modal modal-selector hide"></div>');

      $target.modal_form({}, $trigger);
      this.newInstance($target[0], $.extend({
        $trigger: $trigger
      }, options));
      return $target;
    }
  }, {
    init: function () {
      this.element.html(can.view(this.options.component, this.options));
    }
  });

  $('body').on('click', selectors.join(', '), function (ev, disableMapper) {
    var btn = $(ev.currentTarget);
    var data = {};
    var isSearch;

    _.each(btn.data(), function (val, key) {
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
      GGRC.Controllers.MapperModal.launch(btn, _.extend({
        object: btn.data('join-object-type'),
        type: btn.data('join-option-type'),
        'join-object-id': btn.data('join-object-id'),
        'search-only': isSearch,
        template: {
          title: isSearch ?
            '/static/mustache/base_objects/modal/search_title.mustache' : ''
        }
      }, data));
    }
  });
})(window.can, window.can.$);
