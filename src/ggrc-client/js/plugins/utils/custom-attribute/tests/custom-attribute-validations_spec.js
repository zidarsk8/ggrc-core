/*
Copyright (C) 2019 Google Inc.
Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import * as validationActions from '../custom-attribute-validations';
import CustomAttributeObject from '../custom-attribute-object';

describe('hasEmptyMandatoryValue() function', () => {
  let injected;
  let caDef;

  beforeEach(function () {
    caDef = new can.Map();
    injected = {
      currentCaObject: new CustomAttributeObject(
        new can.Map(),
        caDef,
        new can.Map()
      ),
    };
  });

  describe('when passed current caObject has an empty value and is mandatory',
    () => {
      beforeEach(function () {
        injected.currentCaObject.value = null;
        caDef.attr('mandatory', true);
      });

      it('returns state where hasEmptyMandatoryValue equals to true',
        function () {
          const result = validationActions.hasEmptyMandatoryValue(injected);
          expect(result.hasEmptyMandatoryValue).toBe(true);
        });
    });

  it('returns state where hasEmptyMandatoryValue equals to false by default',
    function () {
      const result = validationActions.hasEmptyMandatoryValue(injected);
      expect(result.hasEmptyMandatoryValue).toBe(false);
    });
});

describe('hasGCAErrors() function', () => {
  let injected;
  let caDef;
  let caValue;

  beforeEach(function () {
    caValue = new can.Map();
    caDef = new can.Map();
    injected = {
      currentCaObject: new CustomAttributeObject(
        new can.Map(),
        caDef,
        caValue
      ),
    };
  });

  it('returns state where hasGCAErrors equals to true if there are GCA errors',
    function () {
      let result;
      caValue.attr('attribute_value', '');
      caDef.attr('mandatory', true);
      result = validationActions.hasGCAErrors(injected);
      expect(result.hasGCAErrors).toBe(true);
    });

  it('returns state where hasGCAErrors equals to false if there are no ' +
  'GCA errors', function () {
    let result;
    result = validationActions.hasGCAErrors(injected);
    expect(result.hasGCAErrors).toBe(false);
  });
});
