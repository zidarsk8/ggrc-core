/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './rich_text.mustache';

const URL_CLIPBOARD_REGEX = /https?:\/\/[^\s]+/g;
const URL_TYPE_REGEX = /https?:\/\/[^\s]+$/;

GGRC.Components('richText', {
  tag: 'rich-text',
  template: template,
  viewModel: {
    define: {
      placeholder: {
        type: 'string',
        value: ''
      },
      disabled: {
        set(newValue) {
          this.toggle(!newValue);
          return newValue;
        }
      },
      text: {
        type: 'string',
        value: '',
        set(text) {
          text = text || '';
          this.setText(text);
          return text;
        }
      },
      toolbarClasses: {
        type: 'string',
        value: '',
        get() {
          if (!this.attr('hiddenToolbar')) {
            return '';
          }

          if (this.attr('editorHasFocus')) {
            return '';
          }

          return 'rich-text__wrapper-hidden-toolbar';
        }
      }
    },
    tabIndex: '-1',
    hiddenToolbar: false,
    forceShow: false,
    editor: false,
    editorHasFocus: false,
    initEditor(container, toolbarContainer, text) {
      import(/* webpackChunkName: "quill" */'quill').then((Quill)=> {
        let editor = new Quill(container, {
          theme: 'snow',
          bounds: container,
          placeholder: this.attr('placeholder'),
          modules: {
            toolbar: {
              container: toolbarContainer
            },
            clipboard: {
              matchers: [
                [Node.TEXT_NODE, this.urlMatcher]
              ]
            }
          }
        });
        if (text) {
          editor.clipboard.dangerouslyPasteHTML(0, text);
        }
        editor.on('text-change', this.onChange.bind(this));

        if (this.attr('hiddenToolbar')) {
          editor.on('selection-change',
            this.onSelectionChange.bind(this));
        }
        this.attr('editor', editor);
      });
    },
    urlMatcher(node, delta) {
      let matches;
      let ops;
      let str;
      if (typeof (node.data) !== 'string') {
        return;
      }
      matches = node.data.match(URL_CLIPBOARD_REGEX);

      if (matches && matches.length > 0) {
        ops = [];
        str = node.data;
        matches.forEach((match)=> {
          let split = str.split(match);
          let beforeLink = split.shift();
          ops.push({insert: beforeLink});
          ops.push({insert: match, attributes: {link: match}});
          str = split.join(match);
        });
        ops.push({insert: str});
        delta.ops = ops;
      }

      return delta;
    },
    isWhitespace(ch) {
      return (ch === ' ') || (ch === '\t') || (ch === '\n');
    },
    onSelectionChange() {
      let editor = this.attr('editor');
      let activeElement = document.activeElement;

      // checks case when we click on another rich-text component
      // or outside of component
      if (editor.hasFocus() ||
        $(activeElement).closest('rich-text').viewModel() === this) {
        this.attr('editorHasFocus', true);
        return;
      }

      this.attr('editorHasFocus', false);
    },
    onRemoved() {
      let editor = this.getEditor();

      if (this.attr('hiddenToolbar') && editor) {
        editor.off('selection-change');
      }
    },
    onChange(delta) {
      let match;
      let url;
      let ops;
      let text;
      let startIdx;
      let endIdx;
      let editor;
      if (!this.getTextLength()) {
        // Should null text value if this is no content
        return this.attr('text', '');
      }

      if (delta.ops.length === 2 &&
        delta.ops[0].retain &&
        !delta.ops[1].delete &&
        !this.isWhitespace(delta.ops[1].insert)) {
        editor = this.getEditor();
        text = editor.getText();
        startIdx = delta.ops[0].retain;
        while (!this.isWhitespace(text[startIdx - 1]) && startIdx > 0) {
          startIdx--;
        }
        endIdx = delta.ops[0].retain + 1;
        while (!this.isWhitespace(text[endIdx]) && endIdx < text.length) {
          endIdx++;
        }

        match = text.substring(startIdx, endIdx).match(URL_TYPE_REGEX);
        if (match !== null) {
          url = match[0];

          ops = [];
          if (startIdx !== 0) {
            ops.push({retain: startIdx});
          }
          ops = ops.concat([
            {'delete': url.length},
            {insert: url, attributes: {link: url}}
          ]);
          editor.updateContents({
            ops: ops
          });
        }
      }

      return this.attr('text', this.getContent());
    },
    toggle(isDisabled) {
      let editor = this.getEditor();
      if (editor) {
        editor.enable(isDisabled);
      }
    },
    getEditor() {
      return this.attr('editor');
    },
    getTextLength() {
      return this.getText().trim().length;
    },
    /**
     * Returns only text content of the Rich Text
     * @return {String} - plain text value
     */
    getText() {
      return this.getEditor().getText();
    },
    setText(text) {
      let editor = this.getEditor();
      if (editor && !text.length) {
        setTimeout(()=> {
          editor.setText('');
        }, 0);
      }
    },
    /**
     * Returns the whole content of the Rich Text field with HTML content
     * @return {String} - current HTML String
     */
    getContent() {
      return this.getEditor().root.innerHTML;
    }
  },
  events: {
    inserted() {
      let wysiwyg = this.element.find('.rich-text__content')[0];
      let toolbar = this.element.find('.rich-text__toolbar')[0];
      let text = this.viewModel.attr('text');
      this.viewModel.initEditor(wysiwyg, toolbar, text);
    },
    removed() {
      this.viewModel.onRemoved();
    }
  }
});
