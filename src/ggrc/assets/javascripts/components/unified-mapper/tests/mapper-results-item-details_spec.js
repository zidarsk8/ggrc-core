/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.mapperResultsItemDetails', function () {
  'use strict';

  var Component;
  var viewModel;

  beforeEach(function () {
    var init;
    Component = GGRC.Components.get('mapperResultsItemDetails');
    init = Component.prototype.viewModel.init;
    Component.prototype.viewModel.init = undefined;
    viewModel = GGRC.Components.getViewModel('mapperResultsItemDetails');
    Component.prototype.viewModel.init = init;
    viewModel.init = init;
  });

  describe('init() method', function () {
    var instance;
    beforeEach(function () {
      instance = {
        type: 'Control'
      };
      viewModel.attr('instance', instance);
    });
    it('sets correct instance for Snapshot objects', function () {
      var result;
      var snapshotInstance = {
        snapshotObject: 'snapshotObject'
      };
      viewModel.attr('instance', snapshotInstance);
      viewModel.init();
      result = viewModel.attr('instance');
      expect(result).toEqual('snapshotObject');
    });

    it('sets model for non-snapshot objects', function () {
      var result;
      viewModel.init();
      result = viewModel.attr('model');
      expect(result.model_singular)
        .toEqual('Control');
    });
  });
});
