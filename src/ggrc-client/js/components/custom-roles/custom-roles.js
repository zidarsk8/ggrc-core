/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../related-objects/related-people-access-control';
import '../related-objects/related-people-access-control-group';
import '../people/editable-people-group';
import template from './templates/custom-roles.mustache';

export default can.Component.extend({
  tag: 'custom-roles',
  template: template,
  viewModel: {
    define: {
      instance: {
        set(newValue, setValue) {
          const isReadonly = this.isReadOnlyForInstance(newValue);
          this.attr('readOnly', isReadonly);
          setValue(newValue);
        },
      },
    },
    updatableGroupId: null,
    includeRoles: [],
    excludeRoles: [],
    conflictRoles: [],
    orderOfRoles: [],
    readOnly: false,
    isReadOnlyForInstance(instance) {
      if (!instance) {
        return false;
      }

      return instance.class.isProposable;
    },
    // When we delete some role this action can delete another acl role on the backend.
    // In this case we get in response less objects then was in request.
    // But canJs is merging array-attributes not replacing.
    // As result it doesn't remove redundant element.
    filterACL() {
      let filteredACL = this.attr('instance.access_control_list')
        .filter((role) => role.id);

      this.attr('instance.access_control_list').replace(filteredACL);
    },
    save(args) {
      this.attr('updatableGroupId', args.groupId);
      this.attr('instance').save().then(() => {
        this.filterACL();
        this.attr('updatableGroupId', null);
      });
    },
  },
});
