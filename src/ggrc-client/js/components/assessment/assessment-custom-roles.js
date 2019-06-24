/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanComponent from 'can-component';
import '../related-objects/related-people-access-control';
import '../related-objects/related-people-access-control-group';
import '../people/editable-people-group';
import template from './templates/assessment-custom-roles.stache';
import viewModel from '../custom-roles/custom-roles-vm';

export default CanComponent.extend({
  tag: 'assessment-custom-roles',
  view: can.stache(template),
  leakScope: true,
  viewModel: viewModel.extend({
    deferredSave: null,
    onStateChangeDfd: null,
    setInProgress: $.noop(),
    save(args) {
      this.attr('deferredSave').push(() => {
        this.attr('updatableGroupId', args.groupId);
      })
        .then(() => {
          this.filterACL();
        }).always(() => {
          this.attr('updatableGroupId', null);
        });
    },
  }),
});
