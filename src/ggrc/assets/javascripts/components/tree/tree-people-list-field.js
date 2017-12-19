/*
  Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default can.Component.extend({
  tag: 'tree-people-list-field',
  template: '<tree-field {source}="source" {field}="\'email\'"/>',
  viewModel: {
    source: null,
  },
});
