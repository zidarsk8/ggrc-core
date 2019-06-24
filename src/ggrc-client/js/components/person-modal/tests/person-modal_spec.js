/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../person-modal';
import PersonProfile from '../../../models/service-models/person-profile';
import * as UserUtils from '../../../plugins/utils/user-utils';

describe('person-modal component', () => {
  let viewModel;

  beforeAll(() => {
    viewModel = getComponentVM(Component);
  });

  describe('updatePersonProfile() method', () => {
    let profile;

    beforeEach(() => {
      viewModel.attr('instance', {});
      profile = new CanMap({
        save: jasmine.createSpy('save'),
      });
      spyOn(PersonProfile, 'findInCacheById').and.returnValue(profile);
    });

    it('saves profile from cache if it was found there', async (done) => {
      const profileStub = {id: 12345};
      viewModel.attr('instance', {profile: profileStub});

      await viewModel.updatePersonProfile();

      expect(PersonProfile.findInCacheById).toHaveBeenCalledWith(
        profileStub.id
      );
      expect(profile.save).toHaveBeenCalled();
      done();
    });

    it('saves loaded profile if it was not found in cache', async (done) => {
      PersonProfile.findInCacheById.and.returnValue(null);
      spyOn(UserUtils, 'loadPersonProfile').and.returnValue(
        Promise.resolve(profile)
      );

      await viewModel.updatePersonProfile();

      expect(UserUtils.loadPersonProfile).toHaveBeenCalledWith(
        viewModel.attr('instance')
      );
      expect(UserUtils.loadPersonProfile).toHaveBeenCalledBefore(profile.save),
      done();
    });

    it('sets profile\'s send_calendar_events to the value of ' +
    'turnOnCalendarEvents field', async (done) => {
      viewModel.attr('turnOnCalendarEvents', false);

      await viewModel.updatePersonProfile();

      expect(profile.attr('send_calendar_events')).toBe(false);
      done();
    });
  });

  describe('loadPersonProfile() method', () => {
    let profile;

    beforeEach(() => {
      profile = new CanMap();
      spyOn(PersonProfile, 'findInCacheById').and.returnValue(profile);
    });

    it('uses person\'s profile extracted from cache', () => {
      const profileStub = {id: 12345};
      viewModel.attr('instance', {profile: profileStub});

      viewModel.loadPersonProfile();

      expect(PersonProfile.findInCacheById).toHaveBeenCalledWith(12345);
    });

    it('sets turnOnCalendarEvents to the value of profile\'s ' +
    'send_calendar_events field', () => {
      profile.attr('send_calendar_events', true);

      viewModel.loadPersonProfile();

      expect(viewModel.attr('turnOnCalendarEvents')).toBe(true);
    });
  });

  describe('events', () => {
    let events;

    beforeAll(() => {
      events = Component.prototype.events;
    });

    describe('"{instance} created"() event handler', () => {
      let handler;

      beforeEach(() => {
        handler = events['{instance} created'].bind({viewModel});
      });

      it('updates person\'s profile', () => {
        spyOn(viewModel, 'updatePersonProfile');

        handler();

        expect(viewModel.updatePersonProfile).toHaveBeenCalled();
      });
    });

    describe('"{instance} updated"() event handler', () => {
      let handler;

      beforeEach(() => {
        handler = events['{instance} updated'].bind({viewModel});
      });

      it('updates person\'s profile', () => {
        spyOn(viewModel, 'updatePersonProfile');

        handler();

        expect(viewModel.updatePersonProfile).toHaveBeenCalled();
      });
    });

    describe('inserted() event handler', () => {
      let handler;

      beforeEach(() => {
        handler = events.inserted.bind({viewModel});
        spyOn(viewModel, 'loadPersonProfile');
      });

      it('initializes person\'s edit modal if the person isn\'t new', () => {
        viewModel.attr('isNewInstance', false);

        handler();

        expect(viewModel.loadPersonProfile).toHaveBeenCalled();
      });

      it('does nothing for create modal (when the person is new)', () => {
        viewModel.attr('isNewInstance', true);

        handler();

        expect(viewModel.loadPersonProfile).not.toHaveBeenCalled();
      });
    });
  });
});
