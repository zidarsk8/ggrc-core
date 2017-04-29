/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  'use strict';

  /**
   * Util methods for integration with Dashboards.
   */
  GGRC.Utils.Dashboards = (function () {
    var DASHBOARD_URLS = {
      audit: GGRC.AUDIT_DASHBOARD_INTEGRATION_URL
    };

    /**
     * Determine whether dashbord integration is enabled for the model.
     * @param {String} model - The model name
     * @return {Boolean} True or False
     */
    function isDashboardEnabled(model) {
      return !!DASHBOARD_URLS[model];
    }

    /**
     * Get url to a dashboard for the iframe.
     * @param {String} model - The model name
     * @param {Object} instance - The model instance
     * @return {String} Url
     */
    function getDashboardUrl(model, instance) {
      var urlTemplate = DASHBOARD_URLS[model];
      return urlTemplate.replace('{{OBJECT_ID}}', instance.id);
    }

    return {
      isDashboardEnabled: isDashboardEnabled,
      getDashboardUrl: getDashboardUrl
    };
  })();
})(window.GGRC, window.GGRC.Utils.Snapshots);
