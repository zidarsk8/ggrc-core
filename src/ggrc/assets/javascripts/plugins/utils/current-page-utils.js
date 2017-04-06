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

      return queryAPI.makeRequest({data: reqParams})
        .then(function (response) {
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
    // Needs refactoring: should be modified to some solid solution
    function getPageType() {
      return GGRC.pageType ||
      GGRC.page_instance() ? GGRC.page_instance().type : '';
    }

    function isMyAssessments() {
      return getPageType() === 'MY_ASSESSMENTS';
    }

    function isMyWork() {
      return getPageType() === 'MY_WORK';
    }

    function isAdmin() {
      return getPageType() === 'ADMIN';
    }

    function isObjectContextPage() {
      return !getPageType();
    }

    /**
     * Should return list of widgets required for rendering
     * @param {String} modelName - Page Object Model Name
     * @param {String} path - Application location path
     * @return {Object} - widget list object
     */
    function getWidgetList(modelName, path) {
      var widgetList = {};
      var isAssessmentsView;

      if (!modelName) {
        return widgetList;
      }
      widgetList = GGRC.WidgetList.get_widget_list_for(modelName);
      // Needs refactoring: Should be removed and replaced with Routing!!!
      isAssessmentsView = /^\/assessments_view/.test(path);

      // the assessments_view only needs the Assessments widget
      if (isAssessmentsView) {
        widgetList = {assessment: widgetList.assessment};
      }

      return widgetList;
    }

    function getWidgetModels(modelName, path) {
      var widgetList = getWidgetList(modelName, path);
      var defaults = getDefaultWidgets(widgetList, path);

      return defaults.map(function (widgetName) {
        return widgetList[widgetName]
          .content_controller_options.model.shortName;
      });
    }

    function getDefaultWidgets(widgetList, path) {
      var defaults = Object.keys(widgetList);
      // Needs refactoring: Should be removed and replaced with Routing!!!
      var isObjectBrowser = /^\/objectBrowser\/?$/.test(path);

      // Remove info and task tabs from object-browser list of tabs
      if (isObjectBrowser) {
        defaults.splice(defaults.indexOf('info'), 1);
        defaults.splice(defaults.indexOf('task'), 1);
      }
      return defaults;
    }

    return {
      related: relatedToCurrentInstance,
      initMappedInstances: initMappedInstances,
      getPageType: getPageType,
      isMyAssessments: isMyAssessments,
      isMyWork: isMyWork,
      isAdmin: isAdmin,
      isObjectContextPage: isObjectContextPage,
      getWidgetList: getWidgetList,
      getWidgetModels: getWidgetModels,
      getDefaultWidgets: getDefaultWidgets
    };
  })();
})(window.GGRC);
