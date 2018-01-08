/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tag = 'comment-add-button';
  var template = '<button class="btn btn-small btn-gray"' +
    ' ($click)="createComment()">' +
    '<content></content>' +
    '</button>';

  GGRC.Components('commentAddButton', {
    tag: tag,
    template: template,
    viewModel: {
      define: {
        disabled: {
          get: function () {
            return this.attr('isSaving') ||
              !this.attr('value').length ||
              this.attr('isDisabled');
          }
        },
        value: {
          type: 'string',
          value: '',
          set: function (newValue) {
            return newValue || '';
          }
        }
      },
      isDisabled: false,
      isSaving: false,
      createComment: function () {
        var comment;
        var description = this.attr('value');

        if (this.attr('disabled')) {
          return;
        }

        comment = new CMS.Models.Comment({
          description: description,
          created_at: new Date(),
          modified_by: {type: 'Person', id: GGRC.current_user.id}
        });
        // Erase RichText Field after Comment Creation
        this.attr('value', '');

        this.dispatch({
          type: 'commentCreated',
          comment: comment
        });
      }
    }
  });
})(window.can, window.GGRC);
