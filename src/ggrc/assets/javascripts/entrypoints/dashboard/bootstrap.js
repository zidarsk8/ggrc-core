/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {
  getWidgetList,
  getDefaultWidgets,
  getWidgetModels,
  getPageType,
  initCounts,
  initWidgets,
} from '../../plugins/utils/current-page-utils';

var $area = $('.area').first();
var defaults;
var extraPageOptions;
var instance;
var location = window.location.pathname;
var isAssessmentsView;
var isObjectBrowser;
var modelName;
var widgetList;
var widgetModels;

extraPageOptions = {
  Program: {
    page_title: function (controller) {
      return 'GRC Program: ' + controller.options.instance.title;
    }
  },
  Person: {
    page_title: function (controller) {
      var instance = controller.options.instance;
      return /dashboard/.test(window.location) ?
        'GRC: My Work' :
        'GRC Profile: ' +
        (instance.name && instance.name.trim()) ||
        (instance.email && instance.email.trim());
    }
  }
};

isAssessmentsView = /^\/assessments_view/.test(location);
isObjectBrowser = /^\/objectBrowser\/?$/.test(location);

if (/^\/\w+\/\d+($|\?|\#)/.test(location) || /^\/dashboard/.test(location) ||
  isAssessmentsView || isObjectBrowser) {
  instance = GGRC.page_instance();
  modelName = instance.constructor.shortName;

  initWidgets();

  widgetList = getWidgetList(modelName, location);
  defaults = getDefaultWidgets(widgetList, location);
  widgetModels = getWidgetModels(modelName, location);

  if (!isAssessmentsView && getPageType() !== 'Workflow') {
    initCounts(widgetModels, instance.type, instance.id);
  }

  $area.cms_controllers_page_object(can.extend({
    widget_descriptors: widgetList,
    default_widgets: defaults || GGRC.default_widgets || [],
    instance: GGRC.page_instance(),
    header_view: GGRC.mustache_path + '/base_objects/page_header.mustache',
    GGRC: GGRC,  // make the global object available in Mustache templates
    page_title: function (controller) {
      return controller.options.instance.title;
    },
    page_help: function (controller) {
      return controller.options.instance.constructor.table_singular;
    },
    current_user: GGRC.current_user
  }, extraPageOptions[modelName]));
} else {
  $area.cms_controllers_dashboard({
    widget_descriptors: GGRC.widget_descriptors,
    default_widgets: GGRC.default_widgets
  });
}
