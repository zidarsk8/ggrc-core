/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

/**
 * Utils methods for showing standart modals
 */

GGRC.Utils.Modals = (function () {
  /**
   * Shows a warning popup within given options. If a user confirms
   * warning popup, then are called a success callback else - a fail callback.
   *
   * For showing the popup, by default, are used a
   * GGRC.Controllers.Modals.confirm method which controls user actions.
   *
   * Also the user can set own controller by setting controller field in
   * extra param.
   * Warning! Controller should have attached context!
   *
   * Note! It's not recommended to override content_view in the options param,
   * because popup is configured for the default template. If you want to use own
   * logic for confirmation you should explore _setupWarning method and use
   * own templates appropriate to its logic.
   * Be careful with confirmOperationName field - remember that standart
   * GGRC.Controllers.Modals.confirm uses confirmOperationName='confirm'
   * If you sets another value (for example, 'delete'), confirm button will
   * not be able to call success callback. If you want to set it then change
   * a controller with help extra param
   * which will process events for tags with data-{{your confirmOperationName}}
   *
   * @param {Object} options - Sets options for popup. See warning.settings
   *                           with default options.
   * @param {Function} success - Called if a user confirms the warning
   * @param {Function} fail - Called if a user dismiss the warning
   * @param {Object} [extra] - Extra options for warning. See warning.extraSettings
   *                           with default options.
   * @param {Function} extra.controller - Controller with attached context
   * @return {Object} - confirm window
   *
   * @example <caption>Default usage</caption>
   * var options = {
   *  skip_refresh: false,               // refreshes information about instance
   *  modal_title: 'Delete operation',   // title for popup
   *  objectShortInfo: 'Object #21',     // short title for object, for which confirmation is required
   *  modal_description: 'Operation is irreversible', // description for operation
   *  confirmTextForTyping: 'I confirm deletion', // text for confirm input
   *  buttonExtraClasses: 'disabled'     // initially confirm button is disabled
   * };
   *
   * GGRC.Utils.Modals.warning(
   *  options,
   *  function () {
   *    console.log('Success!');
   *  },
   *  function () {
   *    console.log('Fail:(');
   *  }
   * )
   */
  function warning(options, success, fail, extra) {
    var confirmOptions = _.extend({}, warning.settings, options);
    var confirmController;
    var confirm;

    extra = extra || {};

    confirmController = extra.controller || GGRC.Controllers.Modals.confirm;
    confirm = confirmController(confirmOptions, success, fail);

    _setupWarning(confirm, confirmOptions);
    return confirm;
  }

  // default static const settings
  warning.settings = Object.freeze({
    skip_refresh: true, // do not reload info about instance
    modal_title: 'Warning',
    objectShortInfo: 'Object',
    modal_description: '',
    confirmOperationName: 'confirm',
    confirmTextForTyping: 'I confirm',
    content_view:
      GGRC.mustache_path + '/base_objects/confirm_warning.mustache',
    button_view:
      GGRC.mustache_path + '/modals/confirm_button.mustache',
    buttonExtraClasses: 'disabled'
  });

  function _setupWarning(confirm, settings) {
    var confirmText = settings.confirmTextForTyping.toLowerCase();
    var toggleClasses = settings.buttonExtraClasses;
    var operation = settings.confirmOperationName;
    var buttonSelector = '[data-toggle=' + operation + ']';

    confirm.on('change paste keyup', 'input[data-edit=confirm]',
    function (e) {
      var confirmButton = confirm.find(buttonSelector);
      var text = $(this)
        .val()
          .trim()
          .toLowerCase();

      if (text === confirmText) {
        confirmButton.removeClass(toggleClasses);
      } else {
        confirmButton.addClass(toggleClasses);
      }
    });
  }

  return {
    warning: warning
  };
})();
