/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.mapperResultsItemAttrs', function () {
  'use strict';

  let viewModel;
  let DEFAULT_ATTR_TEMPLATE =
    GGRC.mustache_path + '/base_objects/tree-item-attr.mustache';

  beforeEach(function () {
    let Component = GGRC.Components.get('mapperResultsItemAttrs');
    let init = Component.prototype.viewModel.init;
    Component.prototype.viewModel.init = undefined;
    viewModel = GGRC.Components.getViewModel('mapperResultsItemAttrs');
    Component.prototype.viewModel.init = init;
    viewModel.init = init;
  });

  describe('init() method', function () {
    it('sets mustache template path to attributes view of model' +
    ' in viewModel.attrTemplate', function () {
      let result;
      viewModel.attr('modelType', 'Control');
      viewModel.init();
      result = viewModel.attr('attrTemplate');
      expect(result)
        .toEqual(GGRC.mustache_path + '/controls/tree-item-attr.mustache');
    });

    it('sets default mustache template path in viewModel.attrTemplate' +
    ' if attributes view of model not defined', function () {
      let result;
      viewModel.attr('modelType', 'AuditObject');
      viewModel.init();
      result = viewModel.attr('attrTemplate');
      expect(result)
        .toEqual(DEFAULT_ATTR_TEMPLATE);
    });
  });
});
