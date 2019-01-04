/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './inner-nav.stache';
import {getPageInstance} from '../../plugins/utils/current-page-utils';
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
    },
    widgetDescriptors: [],
    widgetList: [],
    /**
     * Converts all descriptors to tabs view models
     */
    handleDescriptors() {
      let descriptors = this.attr('widgetDescriptors');
      let widgets = _.map(descriptors,
        (descriptor) => this.createWidget(descriptor));

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

      let widget = {
        id,
        title,
        type: isObjectVersion(id) ? 'version' : '',
        icon: descriptor.widget_icon,
        href: buildUrl({widget: id}),
        model: descriptor.model,
        order: descriptor.order,
        uncountable: descriptor.uncountable,
      };

      return widget;
    },
    route(path) {

    },
  },
  init() {
    this.viewModel.handleDescriptors();

    router.bind('widget', (ev, newVal) => {
      this.viewModel.route(newVal);
    });
  },
});
