/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.openOriginalLink', function () {
  'use strict';

  describe('originalDeleted property', function () {
    var viewModel;
    var revisions = [
      {id: 1, href: '/revisions/1'},
      {id: 2, href: '/revisions/2'}
    ];

    beforeEach(function () {
      viewModel = GGRC.Components.getViewModel('openOriginalLink');
    });

    function setSpyOnForMakeRequest(returnValue) {
      spyOn(GGRC.Utils.QueryAPI, 'makeRequest')
        .and.returnValue(new can.Deferred().resolve(returnValue));
    }

    function buildRevisionObject(action) {
      return [
        {
          Revision: {
            count: 1,
            values: [
              {action: action}
            ]
          }
        }
      ];
    }

    it('originalDeleted should be false. "revisions" array is empty',
      function (done) {
        viewModel.attr('revisions', []);

        setTimeout(function () {
          expect(viewModel.attr('originalDeleted')).toBe(false);
          done();
        }, 1);
      }
    );

    it('originalDeleted should be false. "modified" action',
      function (done) {
        var makeRequestResponse = buildRevisionObject('modified');

        setSpyOnForMakeRequest(makeRequestResponse);
        viewModel.attr('revisions', revisions);

        setTimeout(function () {
          expect(viewModel.attr('originalDeleted')).toBe(false);
          done();
        }, 1);
      }
    );

    it('originalDeleted should be true. "deleted" action',
      function (done) {
        var makeRequestResponse = buildRevisionObject('deleted');

        setSpyOnForMakeRequest(makeRequestResponse);
        viewModel.attr('revisions', revisions);

        setTimeout(function () {
          expect(viewModel.attr('originalDeleted')).toBe(true);
          done();
        }, 1);
      }
    );
  });
});
