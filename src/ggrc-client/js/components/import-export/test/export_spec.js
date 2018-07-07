/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../export';
import {getComponentVM} from '../../../../js_specs/spec_helpers';

describe('export component', () => {
  describe('getObjectsForExport() method', () => {
    let viewModel;

    beforeEach(function () {
      viewModel = getComponentVM(Component);
    });

    it('returns object with empty expression if filters are empty', () => {
      const panelModel = new can.Map({
        type: 'Program',
        attributes: new can.List(),
        localAttributes: new can.List(),
        mappings: new can.List(),
      });
      const expectedObjects = [{
        object_name: 'Program',
        fields: [],
        filters: {expression: {}},
      }];

      viewModel.panels.push(panelModel);

      expect(viewModel.getObjectsForExport()).toEqual(expectedObjects);
    });
    it('returns object with simple expression if there is one filter', () => {
      const panelModel = new can.Map({
        type: 'Program',
        attributes: new can.List(),
        localAttributes: new can.List(),
        mappings: new can.List(),
        relevant: [{
          filter: {id: 2},
          model_name: 'Program',
        }],
      });
      const expectedObjects = [{
        object_name: 'Program',
        fields: [],
        filters: {expression: {
          object_name: 'Program',
          op: {name: 'relevant'},
          ids: ['2'],
        }},
      }];

      viewModel.panels.push(panelModel);

      expect(viewModel.getObjectsForExport()).toEqual(expectedObjects);
    });
    it('returns object with OR in expression ' +
      'if the second filter has OR operator', () => {
      const panelModel = new can.Map({
        type: 'Program',
        attributes: new can.List(),
        localAttributes: new can.List(),
        mappings: new can.List(),
        relevant: [{
          filter: {id: 2},
          model_name: 'Program',
        }, {
          filter: {id: 3},
          model_name: 'Audit',
          operator: 'OR',
        }],
      });
      const expectedObjects = [{
        object_name: 'Program',
        fields: [],
        filters: {expression: {
          left: {
            object_name: 'Program',
            op: {name: 'relevant'},
            ids: ['2'],
          },
          op: {name: 'OR'},
          right: {
            object_name: 'Audit',
            op: {name: 'relevant'},
            ids: ['3'],
          },
        }},
      }];

      viewModel.panels.push(panelModel);

      expect(viewModel.getObjectsForExport()).toEqual(expectedObjects);
    });
  });
});
