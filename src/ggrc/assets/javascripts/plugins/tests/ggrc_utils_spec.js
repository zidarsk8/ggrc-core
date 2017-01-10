/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

'use strict';

describe('GGRC utils allowed_to_map() method', function () {
  var allowedToMap;
  var fakeOptions;
  var fakeProgram;
  var fakeRequest;
  var fakeAudit;

  beforeAll(function () {
    allowedToMap = GGRC.Utils.allowed_to_map;
  });

  beforeEach(function () {
    fakeOptions = {};
  });

  describe('given an Audit and Program pair', function () {
    beforeEach(function () {
      fakeProgram = new CMS.Models.Program({type: 'Program'});
      fakeAudit = new CMS.Models.Audit({type: 'Audit'});

      spyOn(GGRC.Mappings, 'get_canonical_mapping_name')
        .and.returnValue('audits');

      spyOn(Permission, 'is_allowed_for').and.returnValue(true);
    });

    it('returns false for Audit as source and Program as target', function () {
      var result = allowedToMap(fakeAudit, fakeProgram, fakeOptions);
      expect(result).toBe(false);
    });

    it('returns false for Program as source and Audit as target', function () {
      var result = allowedToMap(fakeProgram, fakeAudit, fakeOptions);
      expect(result).toBe(false);
    });
  });

  describe('given a Person instance', function () {
    var origShortName;
    var otherInstance;
    var person;

    beforeAll(function () {
      origShortName = can.Model.shortName;
      can.Model.shortName = 'cacheable';
    });

    afterAll(function () {
      can.Model.shortName = origShortName;
    });

    beforeEach(function () {
      person = new CMS.Models.Person({type: 'Person'});
      otherInstance = new can.Model({type: 'Foo'});
    });

    it('returns false for any object', function () {
      var result = allowedToMap(otherInstance, person);
      expect(result).toBe(false);
    });
  });
});

describe('GGRC utils isEmptyCA() method', function () {
  var isEmptyCA;

  beforeAll(function () {
    isEmptyCA = GGRC.Utils.isEmptyCA;
  });

  describe('check undefined value', function () {
    it('returns true for undefined', function () {
      var result = isEmptyCA(undefined);
      expect(result).toBe(true);
    });
  });

  describe('check Rich Text value', function () {
    it('returns true for empty div', function () {
      var result = isEmptyCA('<div></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a line break', function () {
      var result = isEmptyCA('<div><br></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a empty list', function () {
      var result = isEmptyCA('<div><ul><li></li></ul></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a empty paragraph', function () {
      var result = isEmptyCA('<div><p></p></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns false for div with the text', function () {
      var result = isEmptyCA('<div>Very important text!</div>', 'Rich Text');
      expect(result).toBe(false);
    });

    it('returns false for not empty list', function () {
      var result = isEmptyCA('<div><ul><li>One</li><li>Two</li></ul></div>',
        'Rich Text');
      expect(result).toBe(false);
    });
  });

  describe('check Checkbox value', function () {
    it('returns false for unchecked', function () {
      var result = isEmptyCA('0', 'Checkbox');
      expect(result).toBe(true);
    });

    it('returns true for checked', function () {
      var result = isEmptyCA('1', 'Checkbox');
      expect(result).toBe(false);
    });
  });

  describe('check Text value', function () {
    it('returns false for not empty', function () {
      var result = isEmptyCA('some text', 'Text');
      expect(result).toBe(false);
    });

    it('returns true for empty', function () {
      var result = isEmptyCA('', 'Text');
      expect(result).toBe(true);
    });
  });

  describe('check Map:Person type', function () {
    it('returns false for selected', function () {
      var result = isEmptyCA('Person', 'Map:Person');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      var result = isEmptyCA('', 'Map:Person');
      expect(result).toBe(true);
    });

    it('returns true for not selected cav', function () {
      var result = isEmptyCA('', 'Map:Person', {attribute_object: null});
      expect(result).toBe(true);
    });

    it('returns false for selected cav', function () {
      var result = isEmptyCA('', 'Map:Person', {attribute_object: 'Person'});
      expect(result).toBe(false);
    });
  });

  describe('check Date type', function () {
    it('returns false for selected', function () {
      var result = isEmptyCA('01/01/2016', 'Date');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      var result = isEmptyCA('', 'Date');
      expect(result).toBe(true);
    });
  });

  describe('check Dropdown type', function () {
    it('returns false for selected', function () {
      var result = isEmptyCA('value', 'Dropdown');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      var result = isEmptyCA('', 'Dropdown');
      expect(result).toBe(true);
    });
  });

  describe('check invalid type', function () {
    it('returns false for invalid type', function () {
      var result = isEmptyCA('some value', 'Invalid');
      expect(result).toBe(false);
    });
  });
});

describe('GGRC utils getRelatedObjects() method', function () {
  it('returns related object only for second tier', function () {
    var result = GGRC.Utils.getRelatedObjects(1);
    expect(result).toEqual(jasmine.any(Object));
    expect(result.mapping).toEqual('related_objects');
    expect(result.draw_children).toBeFalsy();
    expect(result.child_options).toEqual([{}]);
  });

  it('returns related objects for second and third tier', function () {
    var result = GGRC.Utils.getRelatedObjects(2);
    expect(result).toEqual(jasmine.any(Object));
    expect(result.mapping).toEqual('related_objects');
    expect(result.draw_children).toBeTruthy();
    expect(result.child_options).toEqual(jasmine.any(Object));
    expect(result.child_options[0].draw_children).toBeFalsy();
    expect(result.child_options[0].mapping).toEqual('related_objects');
  });
});

describe('GGRC utils getMappableTypes() method', function () {
  var mapper;

  beforeAll(function () {
    var canonicalMappings = {};
    var OBJECT_TYPES = [
      'DataAsset', 'Facility', 'Market', 'OrgGroup', 'Vendor', 'Process',
      'Product', 'Project', 'System', 'Regulation', 'Policy', 'Contract',
      'Standard', 'Program', 'Issue', 'Control', 'Section', 'Clause',
      'Objective', 'Audit', 'Assessment', 'AccessGroup',
      'Document', 'Risk', 'Threat'
    ];
    mapper = GGRC.Utils.getMappableTypes;
    OBJECT_TYPES.forEach(function (item) {
      canonicalMappings[item] = {};
    });
    spyOn(GGRC.Mappings, 'get_canonical_mappings_for')
      .and.returnValue(canonicalMappings);
  });

  it('excludes the References type from the result', function () {
    var result = mapper('Reference');
    expect(_.contains(result, 'Reference')).toBe(false);
  });
  it('returns no results for Person', function () {
    var result = mapper('Person');
    expect(result.length).toBe(0);
  });
  it('returns no results for AssessmentTemplate', function () {
    var result = mapper('AssessmentTemplate');
    expect(result.length).toBe(0);
  });
  it('always returns whitelisted items', function () {
    var whitelisted = ['Hello', 'World'];
    var result = mapper('AssessmentTemplate', {
      whitelist: whitelisted
    });
    expect(_.intersection(result, whitelisted)).toEqual(whitelisted);
  });
  it('always remove forbidden items', function () {
    var forbidden = ['Policy', 'Process', 'Product', 'Program'];
    var list = mapper('DataAsset');
    var result = mapper('DataAsset', {
      forbidden: forbidden
    });
    expect(_.difference(list, result).sort()).toEqual(forbidden.sort());
  });
  it('always leave whitelisted and remove forbidden items', function () {
    var forbidden = ['Policy', 'Process', 'Product', 'Program'];
    var whitelisted = ['Hello', 'World'];
    var list = mapper('DataAsset');
    var result = mapper('DataAsset', {
      forbidden: forbidden,
      whitelist: whitelisted
    });
    var input = _.difference(list, result).concat(_.difference(result, list));
    var output = forbidden.concat(whitelisted);

    expect(input.sort()).toEqual(output.sort());
  });
});

describe('GGRC utils isMappableType() method', function () {
  it('returns false for Person and any type', function () {
    var result = GGRC.Utils.isMappableType('Person', 'Program');
    expect(result).toBe(false);
  });
  it('returns false for AssessmentTemplate and  any type', function () {
    var result = GGRC.Utils.isMappableType('AssessmentTemplate', 'Program');
    expect(result).toBe(false);
  });
  it('returns true for Program and Control', function () {
    var result = GGRC.Utils.isMappableType('Program', 'Control');
    expect(result).toBe(true);
  });
});
