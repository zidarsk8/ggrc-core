/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: vraj@reciprocitylabs.com
 * Maintained By: vraj@reciprocitylabs.com
 */

(function(can, $) {

GGRC.Controllers.Modals("GGRC.Controllers.Delete", {},
  {
  init : function() {
    this._super();
  }

  , "{$footer} a.btn[data-method=delete] click" : function(el, ev) {
    var that = this;
    this.bindXHRToButton(this.options.instance.destroy().done(function(instance) {
      el.trigger("ajax:flash", { success : instance.display_name() +  ' deleted successfully'});
      that.element.trigger("modal:success", that.options.instance);
    }), el);
  }

});

})(window.can, window.can.$);
