/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../related-objects/related-people-access-control';
import '../related-objects/related-people-access-control-group';
import '../people/deletable-people-group';
import '../unarchive_link';
import template from './templates/mapper-results-item-details.mustache';

export default can.Component.extend({
  tag: 'mapper-results-item-details',
  template,
  viewModel: {
    init() {
      let instance = this.attr('instance');
      if (instance.snapshotObject) {
        this.attr('instance', instance.snapshotObject);
      } else {
        this.attr('model', CMS.Models[instance.type]);
      }
    },
    item: null,
    instance: null,
    model: null,
    isMapperDetails: true,
    adminRole: ['Admin'],
    deletableAdmin: false,
  },
});
