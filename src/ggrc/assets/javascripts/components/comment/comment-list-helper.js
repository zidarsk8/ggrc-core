/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function () {
  Mustache.registerHelper('if_comment_list_ready',
    function (instance, options) {
      var commentsMapping = Mustache.resolve(instance)
        .get_mapping('comments');

      var commentsDfd = new $.Deferred();

      var resolveCommentsDfd = function () {
        commentsDfd.resolve();
        commentsMapping.unbind('length', resolveCommentsDfd);
      };

      commentsMapping.bind('length', resolveCommentsDfd);

      return Mustache.defer_render('span', function () {
        return options.fn(options.contexts);
      }, commentsDfd);
    });
})();
