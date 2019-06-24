/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import {loadPersonProfile} from '../../plugins/utils/user-utils';
import PersonProfile from '../../models/service-models/person-profile';

const viewModel = CanMap.extend({
  instance: null,
  isNewInstance: false,
  turnOnCalendarEvents: true,
  async updatePersonProfile() {
    const instance = this.attr('instance');
    let profile = PersonProfile.findInCacheById(instance.attr('profile.id'));

    // If we use "Create" modal then profile might be empty.
    // It's generated on BE after person creation. Because of this,
    // profile should be loaded.
    if (!profile) {
      profile = await loadPersonProfile(instance);
    }

    profile
      .attr('send_calendar_events', this.attr('turnOnCalendarEvents'))
      .save();
  },
  loadPersonProfile() {
    // Profile is loaded in the moment of modal initialization via person's
    // form_preload method
    const profile = PersonProfile.findInCacheById(
      this.attr('instance.profile.id')
    );
    this.attr('turnOnCalendarEvents', profile.attr('send_calendar_events'));
  },
});

const events = {
  '{instance} created'() {
    this.viewModel.updatePersonProfile();
  },
  '{instance} updated'() {
    this.viewModel.updatePersonProfile();
  },
  inserted() {
    const viewModel = this.viewModel;

    // If we open Edit modal then person profile should be loaded
    if (!viewModel.attr('isNewInstance')) {
      viewModel.loadPersonProfile();
    }
  },
};

export default CanComponent.extend({
  tag: 'person-modal',
  leakScope: true,
  viewModel,
  events,
});
