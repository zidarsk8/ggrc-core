/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import viewModel from '../view-models/people-group-vm';

export default GGRC.Components('deletablePeopleGroup', {
  tag: 'deletable-people-group',
  template: can.view(
    GGRC.mustache_path +
    '/components/people/deletable-people-group.mustache'
  ),
  viewModel,
});
