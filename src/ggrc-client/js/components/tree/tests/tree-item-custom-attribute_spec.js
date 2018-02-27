/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {helpers} from './../tree-item-custom-attribute';

describe('helpers.getCustomAttrValue', () => {
  let helper;
  let fakeInstance;
  let fakeOptions;
  let fakeCustomAttrDefs;
  let origValue;
  let actual;

  beforeAll(() => {
    helper = helpers.getCustomAttrValue;

    can.Model.Cacheable.extend('CMS.Models.DummyModel', {
      is_custom_attributable: true,
    }, {});

    fakeCustomAttrDefs = [{
      definition_type: 'control',
      id: 3,
      attribute_type: '',
      title: 'Type',
    },
    {
      definition_type: 'control',
      title: 'CheckBox',
      attribute_type: 'Checkbox',
      id: 4,
    },
    {
      definition_type: 'control',
      title: 'Start Date',
      attribute_type: 'Date',
      id: 5,
    },
    {
      definition_type: 'control',
      title: 'Text',
      attribute_type: 'Text',
      id: 6,
    },
    {
      definition_type: 'control',
      title: 'Rich Text',
      attribute_type: 'Rich Text',
      id: 7,
    },
    {
      definition_type: 'control',
      title: 'Persons',
      attribute_type: 'Map:Person',
      id: 8,
    },
    {
      definition_type: 'control',
      title: 'Date',
      attribute_type: 'Date',
      id: 9,
    },
    {
      definition_type: 'control',
      title: 'Dropdown',
      attribute_type: 'Dropdown',
      id: 10,
    }];
    fakeInstance = new CMS.Models.DummyModel({
      custom_attribute_definitions: fakeCustomAttrDefs,
    });
    origValue = GGRC.custom_attr_defs;
    GGRC.custom_attr_defs = fakeCustomAttrDefs;
  });

  afterAll(() => {
    GGRC.custom_attr_defs = origValue;
    delete CMS.Models.DummyModel;
  });

  beforeEach(() => {
    fakeOptions = {};
  });

  it('return correct value if there is ca value with certain caId',
    function () {
      const caId = 3;
      const value = 'correctValue';
      fakeInstance.customAttr(caId, value);
      actual = helper(fakeInstance, caId, fakeOptions);
      expect(actual).toBe(value);
    });

  describe('return an empty string', () => {
    it('if ca value is empty', function () {
      const caId = 3;
      fakeInstance.customAttr(caId, null);
      actual = helper(fakeInstance, caId, fakeOptions);
      expect(actual).toBe('');
    });

    it('if caObject was not found', function () {
      const caId = 10000;
      actual = helper(fakeInstance, caId, fakeOptions);
      expect(actual).toBe('');
    });
  });

  describe('for caObject of Checkbox type', () => {
    it('returns "Yes" if ca value is true',
      function () {
        const caId = 4;
        fakeInstance.customAttr(caId, true);
        actual = helper(fakeInstance, caId, fakeOptions);
        expect(actual).toEqual('Yes');
      });

    it('returns "No" if ca value is false',
      function () {
        const caId = 4;
        fakeInstance.customAttr(caId, false);
        actual = helper(fakeInstance, caId, fakeOptions);
        expect(actual).toEqual('No');
    });
  });

  describe('for caObject of Date type', () => {
    it('returns formatted date when CAD was found', function () {
      const caId = 9;
      const expected = 'expected date';
      const attrValue = '2017-09-30';
      spyOn(GGRC.Utils, 'formatDate')
        .and.returnValue(expected);

      fakeInstance.customAttr(caId, attrValue);
      actual = helper(fakeInstance, caId, fakeOptions);

      expect(actual).toBe(expected);
      expect(GGRC.Utils.formatDate)
        .toHaveBeenCalledWith(attrValue, true);
    });
  });

  describe('for caObject of Dropdown type', () => {
    it('returns caObject value', function () {
      const caId = 10;
      const value = 'Choice 1';
      fakeInstance.customAttr(caId, value);
      actual = helper(fakeInstance, caId, fakeOptions);
      expect(actual).toBe(value);
    });
  });

  describe('for caObject of Text type', () => {
    it('returns caObject value', function () {
      const caId = 6;
      const value = 'Some text';
      fakeInstance.customAttr(caId, value);
      actual = helper(fakeInstance, caId, fakeOptions);
      expect(actual).toBe(value);
    });
  });

  describe('for caObject of Rich Text type', () => {
    it('returns caObject value', function () {
      const caId = 7;
      const value = '<strong>some text</strong>';
      fakeInstance.customAttr(caId, value);
      actual = helper(fakeInstance, caId, fakeOptions);
      expect(actual).toBe(value);
    });
  });
});
