/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './inner-nav.stache';
import {
  getPageInstance,
  isAdmin,
} from '../../plugins/utils/current-page-utils';
import {getCounts} from '../../plugins/utils/widgets-utils';
import router, {buildUrl} from '../../router';
import {isObjectVersion} from '../../plugins/utils/object-versions-utils';

export default can.Component.extend({
  tag: 'inner-nav',
  template,
  viewModel: {
    define: {
      instance: {
        get() {
          return getPageInstance();
        },
      },
      counts: {
        get() {
          return getCounts();
        },
      },
      isAuditScope: {
        get() {
          return this.attr('instance.type') === 'Audit';
        },
      },
      showTabs: {
        get() {
          let counts = this.attr('counts');
          let isEmptyCounts = can.isEmptyObject(counts.attr());
          return !isEmptyCounts || isAdmin();
        },
      },
    },
    activeWidget: null,
    widgetDescriptors: [],
    widgetList: [],
    /**
     * Converts all descriptors to tabs view models
     */
    handleDescriptors() {
      let descriptors = this.attr('widgetDescriptors');
      let widgets = _.map(descriptors,
        (descriptor) => this.createWidget(descriptor));

      widgets = _.sortBy(widgets, ['order', 'title']);

      this.attr('widgetList', widgets);
    },
    /**
     * Creates tab's view model
     * @param {Objbect} descriptor widget descriptor
     * @return {Object} view model
     */
    createWidget(descriptor) {
      let id = descriptor.widget_id;
      let widgetName = descriptor.widget_name;
      let title = typeof widgetName === 'function'
        ? widgetName() : widgetName;
      let countsName = descriptor.countsName ||
        (descriptor.content_controller_options &&
          descriptor.content_controller_options.countsName) ||
        descriptor.model.shortName;

      let widget = {
        id,
        title,
        type: isObjectVersion(id) ? 'version' : '',
        icon: descriptor.widget_icon,
        href: buildUrl({widget: id}),
        model: descriptor.model,
        order: descriptor.order,
        uncountable: descriptor.uncountable,
        forceRefetch: descriptor.forceRefetch,
        hasCount: false,
        count: 0,
        countsName: !descriptor.uncountable ? countsName : '',
      };

      return widget;
    },
    /**
     * Handles selecting tab
     * @param {string} widgetId selected widget id
     */
    route(widgetId) {
      let widget = this.findWidgetById(widgetId);
      if (!widget && this.attr('widgetList').length) {
        let widgetId = this.attr('widgetList')[0].id;
        router.attr('widget', widgetId);
        return;
      }

      if (widget) {
        this.attr('activeWidget', widget);
        this.dispatch({type: 'activeChanged', widget});
      }
    },
    /**
     * Searches widget by Id in widgetList collection
     * @param {string} widgetId widget id
     * @return {can.Map} widget
     */
    findWidgetById(widgetId) {
      return _.find(this.attr('widgetList'),
        (widget) => widget.id === widgetId);
    },
    /**
     * Searches widget by countName in widgetList collection
     * @param {string} countsName counts name prop in widget
     * @return {can.Map} widget
     */
    findWidgetByCountsName(countsName) {
      return _.find(this.attr('widgetList'),
        (widget) => widget.countsName === countsName);
    },
    /**
     * Sets objects count for widget
     * @param {string} name countsName prop in widget
     * @param {*} count objects count
     */
    setWidgetCount(name, count) {
      let widget = this.findWidgetByCountsName(name);
      if (widget) {
        widget.attr({
          count,
          hasCount: true,
        });
      }
    },
  },
  init() {
    this.viewModel.handleDescriptors();
  },
  events: {
    inserted() {
      router.bind('widget', (ev, newVal) => {
        this.viewModel.route(newVal);
      });

      this.viewModel.route(router.attr('widget'));
    },
    '{counts} change'(counts, event, name, action, count) {
      this.viewModel.setWidgetCount(name, count);
    },
  },
});
