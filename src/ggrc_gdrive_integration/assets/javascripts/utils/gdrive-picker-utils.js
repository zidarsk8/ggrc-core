/*
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  'use strict';

  /**
   * Util methods for custom attributes.
   */
  GGRC.Utils.GDrivePicker = (function () {
    /**
     * Removes picker component after file is picked or cancel is clicked.
     * This shuold be called last from pickerCallback function
     * @param  {Object} picker Picker object
     * @param  {Object} data GDrive Picker action data
     */
    function ensurePickerDisposed(picker, data) {
      var PICKED = google.picker.Action.PICKED;
      var ACTION = google.picker.Response.ACTION;
      var CANCEL = google.picker.Action.CANCEL;

      // sometimes pickerCallback is called with data == { action: 'loaded' }
      // which is not described in the Picker API Docs
      if ( data[ACTION] === PICKED || data[ACTION] === CANCEL ) {
        picker.dispose();
      }
    }

    return {
      ensurePickerDisposed: ensurePickerDisposed,
    };
  })();
})(window.GGRC);
