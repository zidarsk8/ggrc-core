/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as TreeViewUtils from './tree-view-utils';
import {
  batchRequests,
  buildParam,
} from './query-api-utils';
import {
  isSnapshotRelated,
} from './snapshot-utils';
import {
  isObjectVersion,
  getWidgetConfigs,
} from './object-versions-utils';
import Person from '../../models/business-models/person';
import WidgetList from '../../modules/widget_list';
import {
  getPageType,
  getPageInstance,
} from './current-page-utils';

let widgetsCounts = new can.Map({});

let CUSTOM_COUNTERS = {
  MY_WORK: () => _getCurrentUser().getWidgetCountForMyWorkPage(),
  ALL_OBJECTS: () => _getCurrentUser().getWidgetCountForAllObjectPage(),
};

function _getCurrentUser() {
  let userId = GGRC.current_user.id;

  return Person.findInCacheById(userId);
}

const widgetModules = [];
function initWidgets() {
  // Ensure each extension has had a chance to initialize widgets
  can.each(widgetModules, function (module) {
    if (module.init_widgets) {
      module.init_widgets();
    }
  });
}

/**
 * Should return list of widgets required for rendering
 * @param {String} modelName - Page Object Model Name
 * @param {String} path - Application location path
 * @return {Object} - widget list object
 */
function getWidgetList(modelName, path) {
  let widgetList = {};
  let isAssessmentsView;

  if (!modelName) {
    return widgetList;
  }
  widgetList = WidgetList.get_widget_list_for(modelName);
  // Needs refactoring: Should be removed and replaced with Routing!!!
  isAssessmentsView = /^\/assessments_view/.test(path);

  // the assessments_view only needs the Assessments widget
  if (isAssessmentsView) {
    widgetList = {
      assessment: widgetList.Assessment,
    };
    widgetList.assessment.treeViewDepth = 0;
  }

  return widgetList;
}

function getWidgetModels(modelName, path) {
  const widgetList = getWidgetList(modelName, path);
  const defaults = getDefaultWidgets(widgetList, path);

  return defaults
    .filter((name) => widgetList[name].widgetType === 'treeview')
    .map((widgetName) => {
      return isObjectVersion(widgetName) ? widgetName :
        widgetList[widgetName].content_controller_options.model.shortName;
    });
}

function getDefaultWidgets(widgetList, path) {
  let defaults = Object.keys(widgetList);
  // Needs refactoring: Should be removed and replaced with Routing!!!
  let isObjectBrowser = /^\/objectBrowser\/?$/.test(path);

  // Remove info tab from object-browser list of tabs
  if (isObjectBrowser) {
    defaults.splice(defaults.indexOf('info'), 1);
  }
  return defaults;
}

/**
 * Counts for related objects.
 *
 * @return {can.Map} Promise which return total count of objects.
 */
function getCounts() {
  return widgetsCounts;
}

function initWidgetCounts(widgets, type, id) {
  let result;

  // custom endpoint we use only in order to initialize counts for all tabs.
  // In order to update counter for individual tab need to use Query API
  if (widgets.length !== 1 && CUSTOM_COUNTERS[getPageType()]) {
    result = CUSTOM_COUNTERS[getPageType()]();
  } else {
    result = _initWidgetCounts(widgets, type, id);
  }

  return result.then((counts) => {
    getCounts().attr(counts);
  });
}

/**
 * Update Page Counts
 * @param {Array|Object} widgets - list of widgets
 * @param {String} type - Type of parent object
 * @param {Number} id - ID of parent object
 * @return {can.Deferred} - resolved deferred object
 */
function _initWidgetCounts(widgets, type, id) {
  // Request params generation logic should be moved in
  // a separate place
  let widgetsObject = getWidgetConfigs(can.makeArray(widgets));

  let params = widgetsObject.map(function (widgetObject) {
    let param;
    let expression = TreeViewUtils
      .makeRelevantExpression(widgetObject.name, type, id);

    if (isSnapshotRelated(type, widgetObject.name) ||
        widgetObject.isObjectVersion) {
      param = buildParam('Snapshot', {}, expression, null,
        GGRC.query_parser.parse('child_type = ' + widgetObject.name));
    } else {
      param = buildParam(widgetObject.name,
        {}, expression, null,
        widgetObject.additionalFilter ?
          GGRC.query_parser.parse(widgetObject.additionalFilter) :
          null
      );
    }

    param.type = 'count';
    return batchRequests(param);
  });

  // Perform requests only if params are defined
  if (!params.length) {
    return can.Deferred().resolve();
  }

  return $.when(...params).then((...data) => {
    let countsMap = {};
    data.forEach(function (info, i) {
      let widget = widgetsObject[i];
      let name = widget.name;
      let countsName = widget.countsName || widget.name;

      if (isSnapshotRelated(type, name) || widget.isObjectVersion) {
        name = 'Snapshot';
      }
      countsMap[countsName] = info[name].total;
    });
    return countsMap;
  });
}

function refreshCounts() {
  let pageInstance = getPageInstance();
  let widgets;
  let location = window.location.pathname;

  if (!pageInstance) {
    return can.Deferred().resolve();
  }

  widgets = getWidgetModels(pageInstance.constructor.shortName, location);

  return initWidgetCounts(widgets, pageInstance.type, pageInstance.id);
}

export {
  getWidgetList,
  getWidgetModels,
  getDefaultWidgets,
  getCounts,
  initWidgetCounts as initCounts,
  refreshCounts,
  widgetModules,
  initWidgets,
};
