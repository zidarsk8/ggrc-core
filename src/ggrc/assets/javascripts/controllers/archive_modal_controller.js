/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  GGRC.Controllers.Modals('GGRC.Controllers.ToggleArchive', {
    defaults: {
      skip_refresh: false
    }
  }, {
    init: function () {
      this._super();
    },
    'a.btn[data-toggle=archive]:not(:disabled) click': function (el, ev) {
      var that = this;
      // Disable the cancel button.
      var cancelButton = this.element.find('a.btn[data-dismiss=modal]');
      var modalBackdrop = this.element.data('modal_form').$backdrop;

      this.bindXHRToButton(this.options.instance.refresh()
        .then(function (instance) {
          instance.archived = true;
          return instance.save();
        })
        .then(function (instance) {
          var parentController =
            $(that.options.$trigger).closest('.modal').control();
          var msg;
          if (parentController) {
            parentController.options.skip_refresh = true;
          }

          msg = instance.display_name() + ' archived successfully';
          $(document.body).trigger('ajax:flash', {success: msg});
          if (that.element) {
            that.element.trigger('modal:success', that.options.instance);
          }

          return new $.Deferred();
        })
        .fail(function (xhr, status) {
          $(document.body).trigger('ajax:flash', {error: xhr.responseText});
        }), el.add(cancelButton).add(modalBackdrop));
    }
  });
})(window.can, window.can.$);
