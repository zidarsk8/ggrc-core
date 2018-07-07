/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../export-panel';
import {getComponentVM} from '../../../../js_specs/spec_helpers';

describe('export-panel component', function () {
  let viewModel;
  let modelAttributeDefenitions = {
    Assessment: [
      {
        display_name: 'Code',
        type: 'property',
        import_only: false,
      },
      {
        display_name: 'Title',
        type: 'unknowType',
      },
      {
        display_name: 'DisplayName',
        type: 'property',
        // should not be added
        import_only: true,
      },
      {
        display_name: 'map:risk versions',
        type: 'mapping',
      },
      {
        // should not be added
        display_name: 'unmap:vendor versions',
        type: 'mapping',
      },
      {
        display_name: 'LCA #1',
        type: 'object_custom',
      },
    ],
  };

  beforeAll(function () {
    viewModel = getComponentVM(Component);
  });

  describe('refreshItems functions', function () {
    let refreshItemsFunction;

    beforeEach(function () {
      let panelModel = new can.Map({
        attributes: new can.List(),
        localAttributes: new can.List(),
        mappings: new can.List(),
        type: 'Assessment',
      });

      viewModel.attr('item', panelModel);
      refreshItemsFunction = viewModel.refreshItems
        .bind(viewModel);

      spyOn(viewModel, 'getModelAttributeDefenitions').and
        .returnValue(modelAttributeDefenitions[viewModel.attr('item.type')]);
    });

    it('refreshItems function should set item', function () {
      let mappingsItem;
      let attributesItem;

      refreshItemsFunction();

      mappingsItem = viewModel.attr('item.mappings')[0];
      attributesItem = viewModel.attr('item.attributes')[0];

      expect(viewModel.attr('item.mappings').length).toEqual(1);
      expect(viewModel.attr('item.attributes').length).toEqual(2);
      expect(viewModel.attr('item.localAttributes').length).toEqual(1);

      expect(mappingsItem.display_name).toEqual('map:risk versions');
      expect(attributesItem.display_name).toEqual('Code');
    });
  });

  describe('filterModelAttributes functions', function () {
    let filterModelAttributesFunc;

    beforeEach(function () {
      filterModelAttributesFunc = viewModel.filterModelAttributes
        .bind(viewModel);
    });

    it('filterModelAttributes should return TRUE', function () {
      let item = modelAttributeDefenitions.Assessment[0];
      let predicate = item.type !== 'mapping';

      expect(filterModelAttributesFunc(item, predicate))
        .toBe(true);
    });

    it('filterModelAttributes should return FALSE. Wrong predicate',
      function () {
        let item = modelAttributeDefenitions.Assessment[0];
        let predicate = item.type === 'mapping';

        expect(filterModelAttributesFunc(item, predicate))
          .toBe(false);
      }
    );

    it('filterModelAttributes should return FALSE. import_only is true',
      function () {
        let item = modelAttributeDefenitions.Assessment[2];
        let predicate = item.type === 'mapping';

        expect(filterModelAttributesFunc(item, predicate))
          .toBe(false);
      }
    );

    it('filterModelAttributes should return FALSE. unmapped item',
      function () {
        let item = modelAttributeDefenitions.Assessment[4];
        let predicate = item.type === 'mapping';

        expect(filterModelAttributesFunc(item, predicate))
          .toBe(false);
      }
    );
  });
});
