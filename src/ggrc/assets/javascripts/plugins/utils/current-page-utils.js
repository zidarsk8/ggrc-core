/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  'use strict';

  /**
   * Util methods for work with Current Page.
   */
  GGRC.Utils.CurrentPage = (function () {
    var queryAPI = GGRC.Utils.QueryAPI;
    var relatedToCurrentInstance = new can.Map({});

    function initMappedInstances(dependentModels, current) {
      var models = can.makeArray(dependentModels);
      var reqParams = [];

      models.forEach(function (model) {
        reqParams.push(queryAPI.buildRelevantIdsQuery(
          model,
          {},
          {
            type: current.type,
            id: current.id,
            operation: 'relevant'
          }));
      });

      return queryAPI.makeRequest({data: reqParams}).then(function (response) {
        models.forEach(function (model, idx) {
          var ids = response[idx][model].ids;
          var map = ids.reduce(function (mapped, id) {
            mapped[id] = true;
            return mapped;
          }, {});
          relatedToCurrentInstance.attr(model, map);
        });
        return relatedToCurrentInstance;
      });
    }

    /**
     * Return a human-friendly name of the object type of the currently
     * active HNB tab.
     *
     * If there is no "active" tab or the tab is not associated with any object
     * type, null is returned.
     *
     * @return {String|null} - a spaced and capizalized object type name
     */
    function activeTabObject() {
      // NOTE: window.CMS might not yed be available when this module is being
      // defined (in tests at  least), thus we cannot simply pass it in, but
      // instead reference it only when this function is invoked.
      var CMS = window.CMS;
      var PATTERN = /^#(\w+?)_widget.*/gi;

      var modelType;
      var parts;
      var tabType;

      var hash = GGRC.Utils.win.location.hash;
      var matchInfo = PATTERN.exec(hash);

      if (!matchInfo) {
        return null;
      }

      tabType = matchInfo[1];  // the content of the first capturing group
      parts = _.chain(tabType.split('_'))
                .map(_.method('toLowerCase'))
                .map(_.capitalize)
                .value();

      modelType = parts.join('');

      if (!CMS.Models[modelType]) {
        return null;
      }

      return parts.join(' ');  // model type with spaces between words
    }

    return {
      activeTabObject: activeTabObject,
      related: relatedToCurrentInstance,
      initMappedInstances: initMappedInstances
    };
  })();
})(window.GGRC);
