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
    var pageType = GGRC.pageType;

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

    function getPageType() {
      return pageType ? pageType : GGRC.page_instance().type;
    }

    function isMyAssessments() {
      return pageType === 'MY_ASSESSMENTS';
    }

    function isMyWork() {
      return pageType === 'MY_WORK';
    }

    function isAdmin() {
      return pageType === 'ADMIN';
    }

    function isObjectContextPage() {
      return !pageType;
    }

    return {
      related: relatedToCurrentInstance,
      initMappedInstances: initMappedInstances,
      getPageType: getPageType,
      isMyAssessments: isMyAssessments,
      isMyWork: isMyWork,
      isAdmin: isAdmin,
      isObjectContextPage: isObjectContextPage
    };
  })();
})(window.GGRC);
