/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../generate-issues-in-bulk-button';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import * as notifierUtils from '../../../plugins/utils/notifiers-utils';
import * as errorsUtils from '../../../plugins/utils/errors-utils';
import Permission from '../../../permission';

describe('generate-issues-in-bulk-button component', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
  });

  describe('viewModel', () => {
    describe('generate() method', () => {
      beforeEach(() => {
        spyOn(viewModel, 'trackStatus');
      });

      it('should set isGeneratingInProgress flag TRUE', () => {
        spyOn(viewModel, 'generateChildrenIssues')
          .and.returnValue(new $.Deferred());

        viewModel.attr('isGeneratingInProgress', false);

        viewModel.generate();

        expect(viewModel.attr('isGeneratingInProgress')).toBeTruthy();
      });

      it('should make a request to generate issues', () => {
        spyOn(viewModel, 'generateChildrenIssues')
          .and.returnValue(new $.Deferred());

        viewModel.generate();

        expect(viewModel.generateChildrenIssues).toHaveBeenCalled();
      });

      it('should show notification if generating in progress', () => {
        spyOn(viewModel, 'generateChildrenIssues')
          .and.returnValue(new $.Deferred().resolve());
        spyOn(notifierUtils, 'notifier');

        viewModel.generate();

        expect(notifierUtils.notifier)
          .toHaveBeenCalledWith('progress', jasmine.any(String));
      });

      it('should start to track status if generating in progress', () => {
        spyOn(viewModel, 'generateChildrenIssues')
          .and.returnValue(new $.Deferred().resolve());

        viewModel.generate();

        expect(viewModel.trackStatus)
          .toHaveBeenCalledWith(jasmine.any(Number));
      });

      it('should set isGeneratingInProgress flag FALSE if error occures',
        () => {
          viewModel.attr('isGeneratingInProgress', false);

          let dfd = new $.Deferred();
          spyOn(viewModel, 'generateChildrenIssues').and.returnValue(dfd);
          spyOn(errorsUtils, 'handleAjaxError');

          viewModel.generate();
          expect(viewModel.attr('isGeneratingInProgress')).toBeTruthy();

          dfd.reject();

          expect(viewModel.attr('isGeneratingInProgress')).toBeFalsy();
        });

      it('should handle ajax error', () => {
        spyOn(viewModel, 'generateChildrenIssues')
          .and.returnValue(new $.Deferred().reject());
        spyOn(errorsUtils, 'handleAjaxError');

        viewModel.generate();

        expect(errorsUtils.handleAjaxError).toHaveBeenCalled();
      });
    });

    describe('trackStatus() method', () => {
      beforeEach(() => {
        spyOn(viewModel, 'checkStatus');
        jasmine.clock().install();
      });

      afterEach(() => {
        jasmine.clock().uninstall();
      });

      it('should check status by timeout', () => {
        const timeout = 100;

        viewModel.trackStatus(timeout);
        jasmine.clock().tick(timeout + 1);

        expect(viewModel.checkStatus).toHaveBeenCalledWith(timeout);
      });

      it('should store timeout id', () => {
        viewModel.attr('timeoutId', null);

        viewModel.trackStatus();

        expect(viewModel.attr('timeoutId')).not.toBeNull();
      });
    });

    describe('checkStatus() method', () => {
      const timeout = 1;
      let dfd;

      beforeEach(() => {
        dfd = new $.Deferred();
        viewModel.attr('isGeneratingInProgress', true);
        spyOn(viewModel, 'getStatus').and.returnValue(dfd);
        spyOn(viewModel, 'trackStatus');
      });

      it('should make a request to get status', () => {
        viewModel.checkStatus(timeout);

        expect(viewModel.getStatus).toHaveBeenCalled();
      });

      it('should continue to track if status is PENDING', () => {
        viewModel.checkStatus(timeout);
        dfd.resolve({status: 'Pending'});

        expect(viewModel.trackStatus).toHaveBeenCalledWith(timeout * 2);
      });

      it('should continue to track if status is RUNNING', () => {
        viewModel.checkStatus(timeout);
        dfd.resolve({status: 'Running'});

        expect(viewModel.trackStatus).toHaveBeenCalledWith(timeout * 2);
      });

      it('should notify if status is SUCCESS', () => {
        spyOn(notifierUtils, 'notifier');

        viewModel.checkStatus(timeout);
        dfd.resolve({status: 'Success'});

        expect(notifierUtils.notifier)
          .toHaveBeenCalledWith('success', jasmine.any(String));
        expect(viewModel.attr('isGeneratingInProgress')).toBeFalsy();
      });

      it('should notify if status is FAILURE', () => {
        spyOn(notifierUtils, 'notifier');

        viewModel.checkStatus(timeout);
        dfd.resolve({status: 'Failure'});

        expect(notifierUtils.notifier)
          .toHaveBeenCalledWith('error', jasmine.any(String));
        expect(viewModel.attr('isGeneratingInProgress')).toBeFalsy();
      });
    });

    describe('checkInitialStatus() method', () => {
      let dfd;

      beforeEach(() => {
        dfd = new $.Deferred();
        spyOn(viewModel, 'getStatus').and.returnValue(dfd);
        spyOn(viewModel, 'trackStatus');
      });

      it('shouid set isGettingInitialStatus flad TRUE', () => {
        viewModel.attr('isGettingInitialStatus', false);

        viewModel.checkInitialStatus();

        expect(viewModel.attr('isGettingInitialStatus')).toBeTruthy();
      });

      it('should make a request to get status', () => {
        viewModel.checkInitialStatus();

        expect(viewModel.getStatus).toHaveBeenCalled();
      });

      it('should start to track if status is PENDING', () => {
        viewModel.attr('isGeneratingInProgress', false);

        viewModel.checkInitialStatus();

        expect(viewModel.attr('isGettingInitialStatus')).toBeTruthy();

        dfd.resolve({status: 'Pending'});

        expect(viewModel.attr('isGeneratingInProgress')).toBeTruthy();
        expect(viewModel.trackStatus).toHaveBeenCalled();
        expect(viewModel.attr('isGettingInitialStatus')).toBeFalsy();
      });

      it('should start to track if status is RUNNING', () => {
        viewModel.attr('isGeneratingInProgress', false);

        viewModel.checkInitialStatus();

        expect(viewModel.attr('isGettingInitialStatus')).toBeTruthy();

        dfd.resolve({status: 'Running'});

        expect(viewModel.attr('isGeneratingInProgress')).toBeTruthy();
        expect(viewModel.trackStatus).toHaveBeenCalled();
        expect(viewModel.attr('isGettingInitialStatus')).toBeFalsy();
      });

      it('should not start to track is status is not Running or Pending',
        () => {
          viewModel.checkInitialStatus();

          expect(viewModel.attr('isGettingInitialStatus')).toBeTruthy();

          dfd.resolve({status: 'any status'});

          expect(viewModel.attr('isGeneratingInProgress')).toBeFalsy();
          expect(viewModel.trackStatus).not.toHaveBeenCalled();
          expect(viewModel.attr('isGettingInitialStatus')).toBeFalsy();
        });
    });
  });

  describe('events', () => {
    describe('"inserted"', () => {
      let event;

      beforeEach(() => {
        spyOn(viewModel, 'checkInitialStatus');
        event = Component.prototype.events['inserted'].bind({viewModel});
      });

      it('should check status if user has permissions', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(true);

        event();

        expect(viewModel.checkInitialStatus).toHaveBeenCalled();
      });

      it('should not check status if user has not permissions', () => {
        spyOn(Permission, 'is_allowed_for').and.returnValue(false);

        event();

        expect(viewModel.checkInitialStatus).not.toHaveBeenCalled();
      });
    });

    describe('"removed"', () => {
      it('should clear timeout when component is removed', () => {
        let timeoutId = 'any timeout id';
        viewModel.attr('timeoutId', timeoutId);
        spyOn(window, 'clearTimeout');

        Component.prototype.events['removed'].apply({viewModel});

        expect(clearTimeout).toHaveBeenCalledWith(timeoutId);
      });
    });
  });
});
