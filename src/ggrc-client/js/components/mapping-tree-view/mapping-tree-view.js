/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './mapping-tree-view.stache';
import Mappings from '../../models/mappers/mappings';

export default can.Component.extend({
  tag: 'mapping-tree-view',
  template,
  leakScope: true,
  viewModel: {
    parentInstance: null,
    mappedObjects: [],
    itemTemplate: GGRC.mustache_path + '/base_templates/subtree.stache',
  },
  init(element) {
    const binding = Mappings
      .getBinding(
        'info_related_objects',
        this.viewModel.parentInstance
      );

    binding.refresh_instances()
      .then((mappedObjects) => {
        this.viewModel.attr('mappedObjects').replace(mappedObjects);
      });

    // We are tracking binding changes, so mapped items update accordingly
    binding.list.on('change', () => {
      this.viewModel.attr('mappedObjects').replace(binding.list);
    });
  },
});
