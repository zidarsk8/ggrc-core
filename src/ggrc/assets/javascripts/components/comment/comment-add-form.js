/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can, CMS) {
  'use strict';

  var tag = 'comment-add-form';
  var template = can.view(GGRC.mustache_path +
    '/components/comment/comment-add-form.mustache');

  /**
   * A component that takes care of adding comments
   *
   */
  GGRC.Components('commentAddForm', {
    tag: tag,
    template: template,
    viewModel: {
      instance: {},
      sendNotifications: true,
      isSaving: false,
      isLoading: false,
      getCommentData: function () {
        var source = this.attr('instance');

        return {
          comment: source.attr('context'),
          send_notification: this.attr('sendNotifications'),
          context: source.context,
          assignee_type: GGRC.Utils.getAssigneeType(source),
          created_at: new Date(),
          modified_by: {type: 'Person', id: GGRC.current_user.id},
          _stamp: Date.now()
        };
      },
      updateComment: function (comment) {
        comment.attr(this.getCommentData());
        return comment;
      },
      afterCreation: function (comment, wasSuccessful) {
        this.attr('isSaving', false);
        this.dispatch({
          type: 'afterCreate',
          items: [comment],
          success: wasSuccessful
        });
        this.attr('instance').dispatch('refreshInstance');
      },
      mapToParent: function (comment, parent) {
        return (new CMS.Models.Relationship({
          context: parent.attr('context') || {id: null},
          source: parent,
          destination: comment
        })).save();
      },
      onCommentCreated: function (e) {
        var comment = e.comment;
        var self = this;
        var parent = self.attr('instance');

        self.attr('isSaving', true);
        comment = self.updateComment(comment);
        self.dispatch({type: 'beforeCreate', items: [comment.attr()]});

        comment.save()
          .done(function (comment) {
            self.mapToParent(comment, parent)
              .done(function () {
                self.afterCreation(comment, true);
              })
              .fail(function () {
                GGRC.Errors.notifier('error', 'Saving has failed');
                self.afterCreation(comment, false);
              });
          })
          .fail(function () {
            GGRC.Errors.notifier('error', 'Saving has failed');
            self.afterCreation(comment, false);
          });
      }
    }
  });
})(window.GGRC, window.can, window.CMS);
