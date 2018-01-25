/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.mapperResultsItemDetails', function () {
  'use strict';

  let Component;
  let viewModel;

  beforeEach(function () {
    let init;
    Component = GGRC.Components.get('mapperResultsItemDetails');
    init = Component.prototype.viewModel.init;
    Component.prototype.viewModel.init = undefined;
    viewModel = GGRC.Components.getViewModel('mapperResultsItemDetails');
    Component.prototype.viewModel.init = init;
    viewModel.init = init;
  });

  describe('init() method', function () {
    let instance;
    beforeEach(function () {
      instance = {
        type: 'Control'
      };
      viewModel.attr('instance', instance);
    });
    it('sets correct instance for Snapshot objects', function () {
      let result;
      let snapshotInstance = {
        snapshotObject: 'snapshotObject'
      };
      viewModel.attr('instance', snapshotInstance);
      viewModel.init();
      result = viewModel.attr('instance');
      expect(result).toEqual('snapshotObject');
    });

    it('sets model for non-snapshot objects', function () {
      let result;
      viewModel.init();
      result = viewModel.attr('model');
      expect(result.model_singular)
        .toEqual('Control');
    });
  });
});
