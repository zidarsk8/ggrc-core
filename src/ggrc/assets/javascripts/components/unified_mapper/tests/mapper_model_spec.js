/*!
  Copyright (C) 2016 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Models.MapperModel', function () {
  'use strict';

  var mapper;

  beforeEach(function () {
    mapper = new GGRC.Models.MapperModel();
  });

  describe('types() method', function () {
    var canonicalMappings;  // a fake return value for a Spy

    beforeAll(function () {
      var OBJECT_TYPES = [
        'DataAsset', 'Facility', 'Market', 'OrgGroup', 'Vendor', 'Process',
        'Product', 'Project', 'System', 'Regulation', 'Policy', 'Contract',
        'Standard', 'Program', 'Issue', 'Control', 'Section', 'Clause',
        'Objective', 'Audit', 'Assessment', 'AccessGroup', 'Request',
        'Document', 'Risk', 'Threat'
      ];

      canonicalMappings = {};

      OBJECT_TYPES.forEach(function (item) {
        canonicalMappings[item] = {};
      });
    });

    beforeEach(function () {
      spyOn(mapper, 'get_forbidden').and.returnValue([]);
      spyOn(mapper, 'get_whitelist').and.returnValue([]);
      spyOn(GGRC.Mappings, 'get_canonical_mappings_for')
        .and.returnValue(canonicalMappings);
    });

    it('excludes the References type from the result', function () {
      var modelNames;

      var result = mapper.types();

      _.forOwn(result, function (groupInfo, groupName) {
        if (groupName === 'all_objects') {
          modelNames = groupInfo.models;
        } else {
          modelNames = _.map(groupInfo.items, 'title_singular');
        }
        expect(_.contains(modelNames, 'Reference')).toBe(false);
      });
    });
  });
});
