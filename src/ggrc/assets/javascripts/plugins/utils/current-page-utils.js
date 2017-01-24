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
        reqParams.push(queryAPI.buildParam(
          model,
          {},
          {
            type: current.type,
            id: current.id,
            operation: 'relevant'
          },
          ['id']));
      });

      return queryAPI.makeRequest({data: reqParams}).then(function (response) {
        models.forEach(function (model, idx) {
          var values = can.makeArray(response[idx][model].values);
          var map = values.reduce(function (mapped, obj) {
            mapped[obj.id] = true;
            return mapped;
          }, {});
          relatedToCurrentInstance.attr(model, map);
        });
        return relatedToCurrentInstance;
      });
    }

    return {
      related: relatedToCurrentInstance,
      initMappedInstances: initMappedInstances
    };
  })();
})(window.GGRC);
