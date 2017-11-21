/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

var viewModel = can.Map.extend({
  data: null,
  isLoading: false,
  define: {
    isObject: {
      type: 'boolean',
      get: function () {
        return _.isObject(this.attr('data'));
      }
    }
  }
});

GGRC.Components('revisionLogData', {
  tag: 'revision-log-data',
  template: can.view(
    GGRC.mustache_path +
    '/components/revision-log/revision-log-data.mustache'
  ),
  viewModel: viewModel
});
