/*
 Copyright (C) 2018 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/review-link.mustache';
import Permission from '../../permission';
const tag = 'review-link';
const mappingName = 'current_approval_cycles';

export default can.Component.extend({
  tag,
  template,
  viewModel: {
    define: {
      hasPermissions: {
        get() {
          const instance = this.attr('instance');

          if (!instance) {
            return false;
          }

          return Permission.is_allowed_for('update', instance);
        },
      },
      isLinkDisabled: {
        get() {
          return this.attr('instance.snapshot') ||
            this.attr('instance.isRevision');
        },
      },
    },
    instance: {},
    mappingExists: false,
    isLoaded: false,
    checkMapping() {
      let instance = this.attr('instance');

      this.attr('isLoaded', false);
      if (!instance || !instance.get_list_counter) {
        return;
      }

      instance.get_list_counter(mappingName)
        .then((count) => {
          if (typeof count === 'function') {
            count = count();
          }
          this.attr('mappingExists', count > 0);
          this.attr('isLoaded', true);
        });
    },
  },
  events: {
    inserted() {
      this.viewModel.checkMapping();
    },
  },
});
