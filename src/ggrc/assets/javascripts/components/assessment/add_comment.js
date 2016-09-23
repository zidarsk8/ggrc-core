/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, GGRC, can, CMS) {
  'use strict';

  var tag = 'assessment-add-comment';
  var template = can.view(GGRC.mustache_path +
    '/components/assessment/add_comment.mustache');
  var defaultState = new can.Map({
    open: false,
    save: false,
    empty: false,
    controls: true
  });
  var defaultPlaceHolderText = 'Enter comment (optional)';
  var types = {
    related_creators: 'creator',
    related_verifiers: 'verifier',
    related_assignees: 'assignee',
    related_requesters: 'requester',
    related_assessors: 'assessor'
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
      caIds: null,
      instance: null,
      commentPlaceHolder: '@',
      isSaving: false,
      comment: {
        notification: false,
        value: '',
        checked: false
      },
      isEmpty: function () {
        return !this.attr('comment.value');
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
        this.attr('comment.value', null);
      },
      removeEmptyMark: function (scope, el) {
        this.attr('state.empty', !el.text().length);
      },
      getCommentData: function () {
        var source = this.attr('instance');
        var description = this.attr('comment.value');
        var sendNotification = this.attr('comment.checked');
        var data;

        data = {
          description: description,
          send_notification: sendNotification,
          context: source.context,
          assignee_type: getAssigneeType(this.attr('instance'))
        };
        // Extra data to map Custom Attribute Value with Comment
        if (this.attr('caIds') && this.attr('caIds.valueId')) {
          data.custom_attribute_revision_upd = {
            custom_attribute_value: {id: this.attr('caIds.valueId')},
            custom_attribute_definition: {id: this.attr('caIds.defId')}
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
        var comment = null;

        if (this.isEmpty()) {
          return;
        }
        this.attr('isSaving', true);

        comment = this.createComment();

        comment.attr(this.getCommentData()).save()
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
      init: function () {
        var scope = this.scope;
        scope.attr('instance', scope.attr('instance') || GGRC.page_instance());
        scope.attr('state', scope.attr('state') || defaultState);
        scope.attr('commentPlaceHolder',
          scope.attr('commentPlaceHolder') || defaultPlaceHolderText);
        scope.attr('comment.checked', scope.attr('instance.send_by_default'));
      },
      '{scope.state} save': function (scope, ev, val) {
        if (val) {
          this.scope.applyState();
        }
      }
    }
  });
})(window._, window.GGRC, window.can, window.CMS);
