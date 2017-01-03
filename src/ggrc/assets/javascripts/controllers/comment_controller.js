/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $, GGRC) {
  'use strict';

  can.Control('GGRC.Controllers.Comments', {
  }, {
    _create_relationship: function (source, destination) {
      if (!destination) {
        return $.Deferred().resolve();
      }

      return new CMS.Models.Relationship({
        source: source.stub(),
        destination: destination,
        context: source.context
      }).save();
    },
    '{CMS.Models.Comment} created': function (model, ev, instance) {
      var parentDfd;
      var permissionRefresh;
      var source;

      if (!(instance instanceof CMS.Models.Comment)) {
        return;
      }

      source = instance._source_mapping || GGRC.page_instance();
      parentDfd = this._create_relationship(source, instance);
      permissionRefresh = Permission.refresh();

      instance.delay_resolving_save_until(
        $.when(parentDfd, permissionRefresh));
    }
  });

  $(function () {
    $(document.body).ggrc_controllers_comments();
  });
})(this.can, this.can.$, this.GGRC);
