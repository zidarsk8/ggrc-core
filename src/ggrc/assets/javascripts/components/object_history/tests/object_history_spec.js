/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe('GGRC.Components.objectHistory', function () {
  'use strict';

  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('objectHistory');
  });

  describe('_computeObjectChanges() method', function () {
    var method;  // the method under test
    var origModelAttrDefs;  // original user-friendly attribute name definitions

    beforeAll(function () {
      var componentInst = {
        _objectChangeDiff: Component.prototype._objectChangeDiff
      };

      method = Component.prototype._computeObjectChanges.bind(componentInst);
    });

    beforeEach(function () {
      // mock global model attribute definitions
      origModelAttrDefs = GGRC.model_attr_defs;
      GGRC.model_attr_defs = {};
    });

    afterEach(function () {
      GGRC.model_attr_defs = origModelAttrDefs;
    });

    it('computes an empty list on empty Revision history', function () {
      var result;
      var revisions = new can.List();
      var expected = [];

      result = method(revisions);

      expect(can.makeArray(result)).toEqual(expected);
    });

    it('includes the modification time in the diff object', function () {
      var revisions = new can.List([
        {
          updated_at: '2016-01-24T10:05:42',
          modified_by: {id: 1},
          content: {}
        },
        {
          updated_at: '2016-01-30T08:15:11',
          modified_by: {id: 1}
        }
      ]);

      var result = method(revisions);

      expect(result.length).toEqual(1);
      expect(result[0].updatedAt).toEqual('2016-01-30T08:15:11');
    });

    it('includes the author of the change(s) in the diff object', function () {
      var revisions = new can.List([
        {
          updated_at: '2016-01-24T10:05:42',
          modified_by: {id: 1},
          content: {}
        },
        {
          updated_at: '2016-01-30T08:15:11',
          modified_by: {id: 7},
          content: {}
        }
      ]);

      var result = method(revisions);

      expect(result.length).toEqual(1);
      expect(result[0].madeBy).toEqual('User 7');
    });

    it('computes diff objects for all successive Revision pairs', function () {
      var actual;
      var expected;

      var revisions = new can.List([
        {
          updated_at: '2016-01-24T10:05:42',
          modified_by: {id: 1},
          content: {
            title: 'Audit 1',
            description: 'first Audit',
            status: 'New'
          }
        },
        {
          updated_at: '2016-01-25T16:36:29',
          modified_by: {id: 5},
          content: {
            title: 'Audit 1.0',
            description: 'This is first audit',
            status: 'New'
          }
        },
        {
          updated_at: '2016-01-30T13:22:59',
          modified_by: {id: 5},
          content: {
            title: 'Audit 1.0',
            description: 'This is first audit',
            status: 'In Progress'
          }
        }
      ]);

      var result = can.makeArray(method(revisions));

      expect(result.length).toEqual(2);

      result[0].changes = can.makeArray(result[0].changes);
      result[1].changes = can.makeArray(result[1].changes);

      result = _.map(result, function (item) {
        return item.attr();  // convert can.List instances to plain objects
      });

      // NOTE: the actual order of the changed fields does not matter,
      // thus the sorting of the list before the assertion
      actual = _.sortBy(result[0].changes, 'fieldName');
      expected = [
        {
          fieldName: 'description',
          origVal: 'first Audit',
          newVal: 'This is first audit'
        },
        {
          fieldName: 'title',
          origVal: 'Audit 1',
          newVal: 'Audit 1.0'
        }
      ];
      expect(actual).toEqual(expected);

      // check the 2nd diff object, too
      actual = _.sortBy(result[1].changes, 'fieldName');
      expected = [
        {
          fieldName: 'status',
          origVal: 'New',
          newVal: 'In Progress'
        }
      ];
      expect(expected).toEqual(expected);
    });

    describe('with model attributes definitions defined', function () {
      beforeEach(function () {
        GGRC.model_attr_defs = {
          Audit: [
            {
              attr_name: 'title',
              display_name: 'Object Name'
            }
          ]
        };
      });

      it('uses the fields\' display names in the diff objects', function () {
        var actual;
        var expected;

        var revisions = new can.List([
          {
            updated_at: '2016-01-25T16:36:29',
            modified_by: {id: 5},
            resource_type: 'Audit',
            content: {
              title: 'Audit 1.0'
            }
          },
          {
            updated_at: '2016-01-30T13:22:59',
            modified_by: {id: 5},
            resource_type: 'Audit',
            content: {
              title: 'My Audit 1.0'
            }
          }
        ]);

        var result = method(revisions);

        expect(result.length).toEqual(1);

        actual = result[0].changes.attr();  // a plain object needed
        expected = [
          {
            fieldName: 'Object Name',
            origVal: 'Audit 1.0',
            newVal: 'My Audit 1.0'
          }
        ];
        expect(actual).toEqual(expected);
      });

      it('omits object fields that are considered internal', function () {
        var match;

        var revisions = new can.List([
          {
            updated_at: '2016-01-25T16:36:29',
            modified_by: {id: 5},
            resource_type: 'Audit',
            content: {
              title: 'Audit 1.0',
              internalField: 'AUDIT-e34a'
            }
          },
          {
            updated_at: '2016-01-30T13:22:59',
            modified_by: {id: 5},
            resource_type: 'Audit',
            content: {
              title: 'Audit 1.0',
              internalField: 'AUDIT-e34a-v2'
            }
          }
        ]);

        var result = method(revisions);

        expect(result.length).toEqual(1);

        // the Audit's internalField does not have a display name defined in
        // GGRC.model_attr_defs, and is thus considered internal, meaning that it
        // should be omitted from the resulting diff object
        match = _.find(result[0].changes, {fieldName: 'internalField'});
        expect(match).toBeUndefined();
      });
    });
  });
});
