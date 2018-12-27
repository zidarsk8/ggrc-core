/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../revision-log';

import RefreshQueue from '../../../models/refresh_queue';

describe('revision-log component', function () {
  let viewModel;

  beforeEach(function () {
    viewModel = getComponentVM(Component);
  });

  describe('defining default scope values', function () {
    it('sets the instance to null', function () {
      expect(viewModel.attr('instance')).toBeNull();
    });

    it('sets revisions to null', function () {
      expect(viewModel.attr('revisions')).toBeNull();
    });
  });

  describe('fetchItems() method', function () {
    let dfdFetchData;

    beforeEach(function () {
      dfdFetchData = new $.Deferred();
      spyOn(viewModel, '_fetchRevisionsData')
        .and.returnValue(dfdFetchData);
    });

    it('assigns true to isLoading', () => {
      viewModel.fetchItems();

      expect(viewModel.attr('isLoading')).toBe(true);
    });

    it('assigns null to revisions', () => {
      viewModel.fetchItems();

      expect(viewModel.attr('revisions')).toBeNull();
    });

    it('displays a toaster error if fetching the data fails', function () {
      let trigger = spyOn($.prototype, 'trigger');

      viewModel.fetchItems();
      dfdFetchData.reject('Server error');

      expect(trigger).toHaveBeenCalledWith(
        'ajax:flash',
        {error: 'Failed to fetch revision history data.'}
      );
    });

    it('assigns fetched revisionsData to revisions attr', () => {
      const revisionsData = [1, 2, 3];

      viewModel.fetchItems();
      dfdFetchData.resolve(revisionsData);

      expect(viewModel.attr('revisions').serialize())
        .toEqual(revisionsData);
    });
  });

  describe('_fetchRevisionsData() method', function () {
    let triggerDfd;
    let compareDfd;

    beforeEach(function () {
      triggerDfd = $.Deferred();
      spyOn(RefreshQueue.prototype, 'trigger').and.returnValue(triggerDfd);
      spyOn(viewModel, '_fetchAdditionalInfoForRevisions');
      compareDfd = $.Deferred();
      spyOn(viewModel, 'getRevisionForCompare').and.returnValue(compareDfd);
    });

    describe('if options.showLastReviewUpdates is false', () => {
      let revisionsDfd;

      beforeEach(() => {
        viewModel.attr('options.showLastReviewUpdates', false);
        revisionsDfd = $.Deferred();
        spyOn(viewModel, 'getAllRevisions').and.returnValue(revisionsDfd);
      });

      it('fetches all revisions', () => {
        viewModel._fetchRevisionsData();

        expect(viewModel.getAllRevisions).toHaveBeenCalled();
      });

      describe('when revisions fetched', () => {
        it('fetches additional info for revisions', () => {
          const revisions = [];
          viewModel._fetchRevisionsData();

          revisionsDfd.resolve(revisions);

          expect(viewModel._fetchAdditionalInfoForRevisions).
            toHaveBeenCalledWith(jasmine.any(RefreshQueue), revisions);
        });
      });
    });

    it('fetches after review revisions ' +
    'if options.showLastReviewUpdates is true', () => {
      viewModel.attr('options.showLastReviewUpdates', true);
      spyOn(viewModel, 'getAfterReviewRevisions').and.returnValue($.Deferred());

      viewModel._fetchRevisionsData();

      expect(viewModel.getAfterReviewRevisions).toHaveBeenCalled();
    });
  });

  describe('changeLastUpdatesFilter(element) method', () => {
    beforeEach(() => {
      spyOn(viewModel, 'fetchItems');
    });

    it('assigns value of "element.checked" to options.showLastReviewUpdates',
      () => {
        const expected = 'value';
        viewModel.attr('options.showLastReviewUpdates', null);
        viewModel.changeLastUpdatesFilter({
          checked: expected,
        });

        expect(viewModel.attr('options.showLastReviewUpdates'))
          .toBe(expected);
      });

    it('assigns 1 to "pageInfo.current"', () => {
      viewModel.attr('pageInfo', {
        current: 123,
      });
      viewModel.changeLastUpdatesFilter({});

      expect(viewModel.attr('pageInfo.current'))
        .toBe(1);
    });
  });

  describe('init() method', () => {
    let init;

    beforeEach(() => {
      init = Component.prototype.init.bind({
        viewModel: viewModel,
      });
      spyOn(viewModel, 'initObjectReview');
      spyOn(viewModel, 'fetchItems');
    });

    it('calls initObjectReview', () => {
      init();

      expect(viewModel.initObjectReview).toHaveBeenCalled();
    });

    it('calls fetchItems', () => {
      init();

      expect(viewModel.fetchItems).toHaveBeenCalled();
    });
  });
});
