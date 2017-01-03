/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $, Quill) {
  'use strict';

  var formats = [
    'bold',
    'italic',
    'link',
    'underline',
    'list',
    'bullet',
    'strike'
  ];
  // We should Add Placeholder functionality
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
      disabled: null,
      formats: formats,
      initEditor: function (wysiwyg, toolbar, text) {
        var editor = new Quill(wysiwyg, {
          theme: 'snow',
          formats: this.attr('formats'),
          modules: {
            'link-tooltip': true,
            toolbar: {
              container: toolbar
            }
          }
        });
        if (text) {
          editor.setHTML(text);
        }
        editor.on('text-change', this.onChange.bind(this));
        this.setEditor(editor);
      },
      onChange: function () {
        if (!this.getTextLength()) {
          // Should null text value if this is no content
          return this.attr('text', null);
        }
        return this.attr('text', this.getContent());
      },
      toggle: function (isDisabled) {
        var editor = this.getEditor().editor;
        var action = isDisabled ? 'disable' : 'enable';
        editor[action]();
      },
      setEditor: function (editor) {
        this.attr('editor', editor);
      },
      getEditor: function () {
        return this.attr('editor');
      },
      getTextLength: function () {
        return this.getText().trim().length;
      },
      /**
       * Returns only text content of the Rich Text
       * @return {String} - plain text value
       */
      getText: function () {
        return this.getEditor().getText();
      },
      /**
       * Returns the whole content of the Rich Text field with HTML content
       * @return {String} - current HTML String
       */
      getContent: function () {
        return this.getEditor().getHTML();
      }
    },
    events: {
      removed: function () {
        if (this.scope.getEditor()) {
          this.scope.getEditor().destroy();
        }
      },
      inserted: function () {
        var wysiwyg = this.element.find('.rich-text__content');
        var toolbar = this.element.find('.rich-text__toolbar');
        this.scope.initEditor(wysiwyg[0], toolbar[0], this.scope.attr('text'));
      },
      toogle: function (scope, ev, isDisabled) {
        if (!scope.getEditor()) {
          return this.destroy();
        }
        scope.toggle(isDisabled);
      },
      '{scope} disabled': 'toggle',
      // if text had been changed to nothing then clear
      '{scope} text': function (scope, ev, text) {
        if (!scope.getEditor()) {
          return this.destroy();
        }
        if (!text) {
          scope.getEditor().setHTML('');
        }
      }
    }
  });
})(window.can, window.can.$, window.Quill);
