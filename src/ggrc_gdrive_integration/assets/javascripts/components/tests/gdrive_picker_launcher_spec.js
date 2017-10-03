/* !
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.gDrivePickerLauncher', function () {
  'use strict';

  var viewModel;

  beforeAll(function () {
    viewModel = GGRC.Components.getViewModel('gDrivePickerLauncher');
    viewModel.attr('assessmentTypeObjects', [
      {revision: {content: {slug: 'CONTROL-345'}}},
      {revision: {content: {slug: 'CONTROL-678'}}},
    ]);
  });

  it('should test sanitizeSlug() method', function () {
    var sanitizationCheck = {
      'abc-test-code-1.CA-865': 'abc-test-code-1-ca-865',
      'AC01.CA-1121': 'ac01-ca-1121',

      'Automated E-Waste Dashboard.CA-935':
        'automated-e-waste-dashboard-ca-935',

      'CA.PCI 1.2.1': 'ca-pci-1-2-1',
      'control-13.CA-855': 'control-13-ca-855',
      'CONTROL-2084.CA-844': 'control-2084-ca-844',
      'PCI 10.4.3.CA-1065': 'pci-10-4-3-ca-1065',
      'REQUEST-957': 'request-957',
      'TV03.2.4.CA': 'tv03-2-4-ca',
      'SM05.CA-1178': 'sm05-ca-1178',
      'ASSESSMENT-12345': 'assessment-12345',
    };

    Object.keys(sanitizationCheck).forEach(function (key) {
      expect(viewModel.sanitizeSlug(key)).toBe(sanitizationCheck[key]);
    });
  });

  it('should test addFileSuffix() method', function () {
    var fakeInstance = new can.Map({
      slug: 'ASSESSMENT-12345',
    });

    var fileNameTransformationMap = {
      'Screenshot 2016-04-29 12.56.30.png':
        'Screenshot 2016-04-29 12.56.30_ggrc_assessment' +
        '-12345_control-345_control-678.png',

      'IMG-9000_ggrc_request-12345.jpg':
        'IMG-9000_ggrc_assessment-12345_control-345_control-678.jpg',
    };

    viewModel.attr('instance', fakeInstance);

    Object.keys(fileNameTransformationMap).forEach(function (key) {
      expect(viewModel.addFileSuffix(key)).toBe(fileNameTransformationMap[key]);
    });
  });
});
