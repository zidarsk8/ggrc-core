/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './people-list-info.mustache';
import '../../models/service-models/role';
import PersonProfile from '../../models/service-models/person-profile';

let viewModel = can.Map.extend({
  instance: null,
  profile: null,
  isOpen: false,
  isHidden: false,
  isRefreshed: false,
  isSaving: false,
  isAttributesDisabled: false,
  async onSendCalendarEventsChange({checked}) {
    const profile = this.attr('profile');

    profile.attr('send_calendar_events', checked);

    this.attr('isSaving', true);
    await profile.save();
    this.attr('isSaving', false);
  },
  refreshInstance() {
    if (this.attr('isRefreshed')) {
      return;
    }

    this.attr('isAttributesDisabled', true);
    this.attr('instance').refresh().then(() => {
      this.attr('isAttributesDisabled', false);
    });
    this.attr('isRefreshed', true);
  },
  async loadPersonProfile() {
    const profile = await PersonProfile.findOne({
      id: this.attr('instance.profile.id'),
    });
    this.attr('profile', profile);
  },
});

export default can.Component.extend({
  tag: 'people-list-info',
  template,
  viewModel,
  events: {
    ' open'() {
      this.viewModel.attr('isHidden', false);
      this.viewModel.attr('isOpen', true);
      this.viewModel.refreshInstance();
      this.viewModel.loadPersonProfile();
    },
    ' close'() {
      this.viewModel.attr('isHidden', true);
    },
  },
});
