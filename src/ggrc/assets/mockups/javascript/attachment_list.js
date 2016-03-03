/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $, Generator) {
  can.Component.extend({
    tag: 'attachment-list',
    template: can.view('/static/mustache/mockup_base_templates/attachment_list.mustache'),
    scope: {
      title: '@',
      icon: '@',
      button: '@',
      types: '@',
      files: new can.List()
    },
    events: {
      inserted: 'updateFiles',
      '{scope.data} add': 'updateFiles',
      '{scope.data} remove': 'updateFiles',
      updateFiles: function () {
        var types = this.scope.attr('types');
        var isNegation = types.charAt(0) === '!';
        var result;
        if (isNegation) {
          types = types.slice(1);
        }
        result = _.reduce(this.scope.attr('data'), function (memo, comment) {
          var attachments = _.filter(comment.attachments, function (attachment) {
            if (isNegation) {
              return attachment.extension !== types;
            }
            return attachment.extension === types;
          });
          if (attachments.length) {
            return memo.concat(_.filter(attachments, function (attachment) {
              return !attachment.attr('deleted');
            }));
          }
          return memo;
        }, []);
        this.scope.attr('files', result);
      },
      '.js-trigger--delete click': function (el, ev) {
        var file = el.data('file');
        file.attr('deleted', true);
        this.updateFiles();
      },
      '.btn-draft click': function (el, ev) {
        var attachments = Generator.get(this.scope.attr('types') === 'url' ? 'url' : 'file');
        return this.scope.attr('data').unshift({
          author: Generator.current.u,
          timestamp: Generator.current.d,
          attachments: attachments,
          comment: ''
        });
      }
    }
  });
})(this.can, this.can.$, GGRC.Mockup.Generator);
