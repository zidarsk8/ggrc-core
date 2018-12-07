/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './notifications-menu-item.mustache';
import NotificationConfig
  from '../../models/service-models/notification-config';

export default can.Component.extend({
  tag: 'notifications-menu-item',
  template,
  viewModel: {
    updateNotifications() {
      NotificationConfig.findActive().then(this.checkActive);
    },
    checkActive(notificationConfigs) {
      let inputs = $('.notify-wrap').find('input');
      let activeNotifications = $.map(notificationConfigs, function (a) {
        if (a.enable_flag) {
          return a.notif_type;
        }
      });
      $.map(inputs, function (input) {
        // Handle the default case, in case notification objects are not set:
        if (notificationConfigs.length === 0) {
          input.checked = input.value === 'Email_Digest';
        } else {
          input.checked = activeNotifications.indexOf(input.value) > -1;
        }
      });
    },
  },
  events: {
    'input[name=notifications] click'(el, ev) {
      let li = $(ev.target).closest('.notify-wrap');
      let active = [];
      let emailDigest = li.find('input[value="Email_Digest"]');
      emailDigest.prop('disabled', true);
      if (emailDigest[0].checked) {
        active.push('Email_Digest');
      }
      NotificationConfig.setActive(active).always(function (response) {
        emailDigest.prop('disabled', false);
      });
    },
    // Don't close the dropdown if clicked on checkbox
    ' click'(el, ev) {
      ev.stopPropagation();
    },
  },
  init() {
    this.viewModel.updateNotifications();
  },
});
