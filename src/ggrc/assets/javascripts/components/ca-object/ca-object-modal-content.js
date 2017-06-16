/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/ca-object/ca-object-modal-content.mustache');

  can.Component.extend({
    tag: 'ca-object-modal-content',
    template: tpl,
    viewModel: {
      define: {
        comment: {
          get: function () {
            return this.attr('content.fields').indexOf('comment') > -1 &&
              this.attr('state.open');
          }
        },
        evidence: {
          get: function () {
            return this.attr('content.fields').indexOf('evidence') > -1 &&
              this.attr('state.open');
          }
        },
        state: {
          value: {
            open: false,
            save: false,
            controls: false
          }
        }
      },
      allSaved: false,
      formSavedDeferred: can.Deferred(),
      content: {
        contextScope: {},
        fields: [],
        title: '',
        type: 'dropdown',
        value: null,
        options: []
      },
      onCommentCreated: function (e) {
        var comment = e.comment;
        var instance = this.attr('instance');
        var context = instance.attr('context');
        var commentUpdate = {
          context: context,
          assignee_type: GGRC.Utils.getAssigneeType(instance)
        };
        var relation = new CMS.Models.Relationship({
          context: context,
          destination: instance
        });
        var addComment = function (data) {
          return comment.attr(data)
            .save()
            .done(function (comment) {
              relation.attr({source: comment.serialize()})
                .save()
                .then(function () {
                  instance.dispatch('refreshInstance');
                });
            });
        };
        var self = this;

        this.attr('content.contextScope.errorsMap.comment', false);
        this.attr('content.contextScope.validation.valid',
          !this.attr('content.contextScope.errorsMap.evidence'));
        this.attr('state.open', false);
        this.attr('state.save', false);

        this.attr('formSavedDeferred').then(function () {
          commentUpdate.custom_attribute_revision_upd = {
            custom_attribute_value:
            {id: self.attr('content.contextScope.valueId')()},
            custom_attribute_definition:
            {id: self.attr('content.contextScope.id')}
          };
          addComment(commentUpdate);
        });
      }
    }
  });
})(window.can, window.GGRC);
