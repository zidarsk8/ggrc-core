/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, GGRC, can, CMS) {
  'use strict';

  var namespace = 'assessment';
  var tag = 'assessment-add-comment';
  var template = can.view(GGRC.mustache_path +
    '/components/' + namespace + '/add_comment.mustache');
  var defaultState = new can.Map({
    open: false,
    save: false,
    empty: false,
    controls: true
  });
  var types = {
    related_creators: 'creator',
    related_verifiers: 'verifier',
    related_assignees: 'assignee',
    related_requesters: 'requester'
  };

  function getAssigneeType(instance) {
    var user = GGRC.current_user;
    var userType = null;

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
        userType = userType ? userType + ',' + type : type;
      }
    });
    return userType;
  }

  /**
   * A component that takes care of adding comments with attachments
   *
   */
  GGRC.Components('assessmentAddComment', {
    tag: tag,
    template: template,
    scope: {
      instance: null,
      commentEl: null,
      notificationEl: null,
      isSaving: false,
      comment: {
        value: ''
      },
      applyState: function () {
        this.saveComment();
        if (!this.attr('state.open')) {
          this.clean();
        }
      },
      save: function () {
        this.attr('state.save', true);
        this.attr('state.empty', false);
      },
      clean: function () {
        if (this.attr('commentEl')) {
          this.attr('commentEl').val('');
        }
      },
      removeEmptyMark: function (el) {
        this.attr('state.empty', !el.val().length);
      },
      getCommentData: function () {
        var source = this.attr('instance');
        var description = this.attr('commentEl').val().trim();
        var sendNotification = this.attr('notificationEl').attr('checked');
        var data;

        if (!description.length) {
          return;
        }

        data = {
          description: description,
          send_notification: sendNotification,
          context: source.context,
          assignee_type: getAssigneeType(this.attr('instance'))
        };
        // Extra data to map Custom Attribute and Custom Attribute Value with Comment
        if (this.attr('instance._modifiedAttribute') &&
          this.attr('instance._modifiedAttribute.valueId')) {
          data.custom_attribute_revision_upd = {
            custom_attribute_value:
              {id: this.attr('instance._modifiedAttribute.valueId')},
            custom_attribute_definition:
              {id: this.attr('instance._modifiedAttribute.caId')}
          };
        }
        return data;
      },
      createComment: function () {
        var comment = CMS.Models.Comment();
        comment._source_mapping = this.attr('instance');
        comment.attr('context', this.attr('instance.context'));
        return comment;
      },
      saveComment: function () {
        var data = this.getCommentData();
        var comment = null;

        if (!data) {
          return;
        }

        this.attr('isSaving', true);

        comment = this.createComment();

        comment.attr(data).save()
          .then(function () {
            return comment.constructor
              .resolve_deferred_bindings(comment);
          }).always(function () {
            this.clean();
            this.attr('isSaving', false);
            this.attr('state.open', false);
            this.attr('state.save', false);
          }.bind(this));
      }
    },
    events: {
      inserted: function () {
        this.scope.attr('commentEl', this.element.find('textarea'));
        this.scope.attr('notificationEl',
          this.element.find('[name=send_notification]'));
      },
      init: function () {
        var scope = this.scope;
        scope.attr('instance', scope.attr('instance') || GGRC.page_instance());
        scope.attr('state', scope.attr('state') || defaultState);
      },
      '{scope.state} save': function (scope, ev, val) {
        if (val) {
          this.scope.applyState();
        }
      },
      'textarea keyup': function (el) {
        this.scope.removeEmptyMark(el);
      }
    }
  });
})(window._, window.GGRC, window.can, window.CMS);
