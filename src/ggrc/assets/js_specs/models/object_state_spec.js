/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('Model states test', function () {
  it('checks if basic objects have the correct statuses property', function () {
    var expectedStatuses = ['Draft', 'Deprecated', 'Active'];
    var basicStateObjects = ['AccessGroup', 'Clause', 'Contract',
        'Control', 'DataAsset', 'Facility', 'Issue', 'Market',
        'Objective', 'OrgGroup', 'Policy', 'Process', 'Product', 'Program',
        'Project', 'Regulation', 'Risk', 'Section', 'Standard', 'System',
        'Threat', 'Vendor'];

    basicStateObjects.forEach(function (object) {
      expect(CMS.Models[object].statuses).toEqual(
          expectedStatuses, 'for object ' + object);
    });
  });
  it('checks if audit has the correct statuses property', function () {
    var expectedStatuses = ['Planned', 'In Progress', 'Manager Review',
        'Ready for External Review', 'Completed'];
    expect(CMS.Models.Audit.statuses).toEqual(expectedStatuses);
  });
  it('checks if assessment has the correct statuses property', function () {
    var expectedStatuses = ['Not Started', 'In Progress', 'Ready for Review',
        'Verified', 'Completed'];
    expect(CMS.Models.Assessment.statuses).toEqual(expectedStatuses);
  });
});
