/*!
  Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe("GGRC utils allowed_to_map() method", function () {
  "use strict";

  var allowed_to_map,  // the method under test
      fakeOptions,
      fakeProgram,
      fakeAudit;

  beforeAll(function () {
    allowed_to_map = GGRC.Utils.allowed_to_map;
  });

  beforeEach(function () {
    fakeOptions = {};

    fakeProgram = new CMS.Models.Program({type: "Program"});
    fakeAudit = new CMS.Models.Audit({type: "Audit"});

    spyOn(GGRC.Mappings, "get_canonical_mapping_name")
      .and.returnValue("audits");

    spyOn(Permission,"is_allowed_for").and.returnValue(true);
  });

  describe("given an Audit and Program pair", function () {
    it("returns false for Audit as source and Program as target", function () {
      var result = allowed_to_map(fakeAudit, fakeProgram, fakeOptions);
      expect(result).toBe(false);
    });

    it("returns false for Program as source and Audit as target", function () {
      var result = allowed_to_map(fakeProgram, fakeAudit, fakeOptions);
      expect(result).toBe(false);
    });
  });

});
