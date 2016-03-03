/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $, Generator) {
  can.Component.extend({
    tag: 'add-comment',
    template: can.view('/static/mustache/mockup_base_templates/add_comment.mustache'),
    scope: {
      attachments: new can.List()
    },
    events: {
      cleanPanel: function () {
        this.scope.attachments.replace([]);
        this.element.find('textarea').val('');
      },
      '.js-trigger-attachdata click': function (el, ev) {
        var type = el.data('type');
        var typeFn = Generator[type];
        if (!typeFn) {
          return;
        }
        this.scope.attachments.push(typeFn());
      },
      '.btn-success click': function (el, ev) {
        var $textarea = this.element.find('.add-comment textarea');
        var text = $.trim($textarea.val());
        var attachments = this.scope.attachments;

        if (!text.length && !attachments.length) {
          return;
        }
        this.scope.data.unshift({
          author: Generator.current.u,
          timestamp: Generator.current.d,
          comment: text,
          attachments: _.map(attachments, function (attachment) {
            return attachment;
          })
        });
        this.cleanPanel();
      }
    }
  });
})(this.can, this.can.$, GGRC.Mockup.Generator);
