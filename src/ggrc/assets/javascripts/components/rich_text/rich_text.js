/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $, Quill) {
  'use strict';

  GGRC.Components('richText', {
    tag: 'rich-text',
    template: can.view(
      GGRC.mustache_path +
      '/components/rich_text/rich_text.mustache'
    ),
    scope: {
      text: null,
      editor: null,
      placeholder: null,
      formats: ['bold', 'italic', 'link', 'underline',
        'list', 'bullet', 'strike'],
      onChange: function (delta, source) {
        this.attr('text', this.attr('editor').getHTML());
      }
    },
    events: {
      inserted: function () {
        var text = this.scope.attr('text');
        var wysiwyg = this.element.find('.rich-text__content');
        var toolbar = this.element.find('.rich-text__toolbar');
        var editor = new Quill(wysiwyg[0], {
          theme: 'snow',
          formats: this.scope.formats,
          modules: {
            'link-tooltip': true,
            toolbar: {
              container: toolbar[0]
            }
          }
        });
        if (text) {
          editor.setHTML(text);
        }
        editor.on('text-change', this.scope.onChange.bind(this.scope));
        this.scope.attr('editor', editor);
      }
    }
  });
})(window.can, window.can.$, window.Quill);
