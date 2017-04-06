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

    function getWidgetList() {
      var pageInstance;
      var modelName;
      var widgetList;
      var isAssessmentsView;
      var location = window.location.pathname;

      pageInstance = GGRC.page_instance();

      if (!pageInstance) {
        return null;
      }
      modelName = pageInstance.constructor.shortName;
      widgetList = GGRC.WidgetList.get_widget_list_for(modelName);
      isAssessmentsView = /^\/assessments_view/.test(location);

      // the assessments_view only needs the Assessments widget
      if (isAssessmentsView) {
        widgetList = {assessment: widgetList.assessment};
      }

      return widgetList;
    }

    function getWidgetModels() {
      var widgetList;
      var defaults;
      var widgetModels;

      widgetList = this.getWidgetList();

      if (!widgetList) {
        return null;
      }
      defaults = getDefaultWidgets(widgetList);

      widgetModels = defaults.map(function (widgetName) {
        return widgetList[widgetName]
        .content_controller_options.model.shortName;
      });

      return widgetModels;
    }

    function getDefaultWidgets(widgetList) {
      var location = window.location.pathname;
      var defaults = Object.keys(widgetList);
      var isObjectBrowser = /^\/objectBrowser\/?$/.test(location);

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
