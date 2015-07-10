/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  can.Control("GGRC.Controllers.MapperModal", {
    defaults: {
      component: GGRC.mustache_path + "/modals/mapper/component.mustache"
    },
    launch: function ($trigger, options) {
      var href = $trigger.attr("data-href") || $trigger.attr("href"),
          modal_id = "ajax-modal-" + href.replace(/[\/\?=\&#%]/g, "-").replace(/^-/, ""),
          $target = $('<div id="' + modal_id + '" class="modal modal-selector hide"></div>');

      $target.modal_form({}, $trigger);
      this.newInstance($target[0], $.extend({ $trigger: $trigger}, options));
      return $target;
    }
  }, {
    init: function() {
      this.element.html(can.view(this.options.component, this.options));
    }
  });

  can.Component.extend({
    tag: "lazy-openclose",
    scope: {
      show: false,
    },
    content: "<content/>",
    init: function() {
      this._control.element.closest(".tree-item").find(".openclose").bind("click", function() {
        this.scope.attr("show", true);
      }.bind(this));
    }
  });
})(window.can, window.can.$);
