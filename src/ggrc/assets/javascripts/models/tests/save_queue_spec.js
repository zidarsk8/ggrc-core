/*!
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.SaveQueue', function () {
  'use strict';

  describe('_process_save_responses() method', function () {
    var bucket;
    var method;  // the method under test

    beforeEach(function () {
      var thisContext = {};

      method = GGRC.SaveQueue._process_save_responses.bind(thisContext);

      bucket = {
        objs: [],
        type: 'audit',
        plural: 'audits',
        background: false,
        save_responses: [],
        in_flight: false
      };
    });

    // a helper function for generating fake response objects as stored in
    // buckets' save_responses list
    function makeResponse(objType, objId) {
      var modelInstance = {
        type: objType,
        id: objId,
        _save: jasmine.createSpy('_save'),
        _dfd: new can.Deferred()
      };

      var response = [
        [modelInstance],
        [
          [201, {audit: modelInstance}]
        ]
      ];

      return response;
    }

    it('clears the given bucket\'s response list', function () {
      var resp = makeResponse('Audit', 1);
      var resp2 = makeResponse('Audit', 2);
      bucket.save_responses = [resp, resp2];

      method(bucket);

      expect(bucket.save_responses).toEqual([]);
    });
  });
});
