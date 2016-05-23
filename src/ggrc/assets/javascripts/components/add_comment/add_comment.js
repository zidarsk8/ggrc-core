/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: ivan@reciprocitylabs.com
  Maintained By: ivan@reciprocitylabs.com
*/

(function (GGRC, can) {
  'use strict';

/**
   * A component that takes care of adding comments with attachments
   *
   */
  GGRC.Components('addComment', {
    tag: 'add-comment',
    template: can.view('/static/mustache/base_templates/add_comment.mustache'),
    scope: {
      attachments: new can.List(),
      parent_instance: null,
      instance: null,
      instance_attr: '@',
      source_mapping: null,
      source_mapping_source: '@',
      mapping: '@',
      deferred: '@',
      isSaving: false,  // is there a save operation currently in progress
      attributes: {},
      list: [],
      // the following are just for the case when we have no object to start with,
      changes: [],
      get_assignee_type: can.compute(function () {
        // TODO: We prioritize order V > A > R
        var types = {
          related_verifiers: 'verifier',
          related_assignees: 'assignee',
          related_requesters: 'requester'
        };
        var instance = this.attr('parent_instance');
        var user = GGRC.current_user;
        var user_type;

        if (!instance || !user) {
          return;
        }
        _.each(types, function (type, mapping) {
          var mappings = instance.get_mapping(mapping);
          if (!mappings.length) {
            return;
          }
          if (_.filter(mappings, function (mapping) {
            return mapping.instance.id === user.id;
          }).length) {
            type = can.capitalize(type);
            user_type = user_type ? (user_type + ',' + type) : type;
          }
        });
        return user_type;
      })
    },
    events: {
      init: function () {
        if (!this.scope.attr('source_mapping')) {
          this.scope.attr('source_mapping', GGRC.page_instance());
        }
        this.newInstance();
      },
      newInstance: function () {
        var instance = CMS.Models.Comment();
        instance._source_mapping = this.scope.attr('source_mapping');
        instance.attr('context', this.scope.attr('parent_instance.context'));
        this.scope.attr('instance', instance);
      },
      cleanPanel: function () {
        this.scope.attachments.replace([]);
        this.element.find('textarea').val('');
      },
      /**
       * The component's click event (happens when the user clicks add comment),
       * takes care of saving the comment with appended evidence.
       */
      '.btn-success click': function (el, ev) {
        var $textarea = this.element.find('.add-comment textarea');
        var description = $.trim($textarea.val());
        var attachments = this.scope.attachments;
        var source = this.scope.source_mapping;
        var instance = this.scope.instance;
        var data;
        var $sendNotification = this.element.find('[name=send_notification]');
        var sendNotification = $sendNotification[0].checked;

        if (!description.length && !attachments.length) {
          return;
        }
        data = {
          description: description,
          send_notification: sendNotification,
          context: source.context,
          assignee_type: this.scope.attr('get_assignee_type')
        };

        this.scope.attr('isSaving', true);

        instance.attr(data).save()
          .then(function () {
            return instance.constructor.resolve_deferred_bindings(instance);
          })
          .then(function () {
            this.newInstance();
            this.cleanPanel();
          }.bind(this))
          .always(function () {
            this.scope.attr('isSaving', false);
          }.bind(this));
      }
    }
  });
})(window.GGRC, window.can);
