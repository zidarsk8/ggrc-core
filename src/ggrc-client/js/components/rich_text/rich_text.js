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
      disabled: {
        set(disabled) {
          let editor = this.attr('editor');
          if (editor) {
            editor.enable(!disabled);
          }
          return disabled;
        }
      },
      hidden: {
        get(){
          let hiddenToolbar = this.attr('hiddenToolbar');
          let hasFocus = this.attr('editorHasFocus')
          return hiddenToolbar && !hasFocus;
        }
      },
      content: {
        set(newContent){
          let oldContent = this.attr('content')
          let editor = this.attr('editor');
          if (editor && (newContent !== oldContent)) {
            this.setContentToEditor(editor, newContent);
          }
          return newContent;
        }
      }
    },
    editor: null,
    placeholder: '',
    hiddenToolbar: false,
    editorHasFocus: false,
    initEditor(container, toolbarContainer) {
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
        this.setContentToEditor(editor, this.attr('content'));
        editor.on('text-change', this.onChange.bind(this));

        if (this.attr('hiddenToolbar')) {
          editor.on('selection-change', this.onSelectionChange.bind(this));
        }
        this.attr('editor', editor);
      });
    },
    setContentToEditor(editor, content) {
      if (content !== editor.root.innerHTML) {
        let delta = editor.clipboard.convert(content);
        editor.setContents(delta);
      }
    },
    urlMatcher(node, delta) {
      if (typeof (node.data) !== 'string') {
        return;
      }

      let matches = node.data.match(URL_CLIPBOARD_REGEX);

      if (matches && matches.length > 0) {
        let ops = [];
        let str = node.data;
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
    onChange(delta, oldDelta) {
      let editor = this.attr('editor');
      // real length without service tags
      let textLength = editor.getText().trim().length;

      // handle and highlight urls
      if (textLength &&
        delta.ops.length === 2 &&
        delta.ops[0].retain &&
        !delta.ops[1].delete &&
        !this.isWhitespace(delta.ops[1].insert)) {

        let text = editor.getText();
        let startIdx = delta.ops[0].retain;
        while (!this.isWhitespace(text[startIdx - 1]) && startIdx > 0) {
          startIdx--;
        }
        let endIdx = delta.ops[0].retain + 1;
        while (!this.isWhitespace(text[endIdx]) && endIdx < text.length) {
          endIdx++;
        }

        let match = text.substring(startIdx, endIdx).match(URL_TYPE_REGEX);
        if (match !== null) {
          let url = match[0];
          let ops = [];
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

      // innerHTML could containe only tags f.e. <p><br></p>
      // we have to save empty string in this case;
      let content = textLength ? editor.root.innerHTML : '';
      this.attr('content', content);
    },
  },
  events: {
    inserted() {
      let wysiwyg = this.element.find('.rich-text__content')[0];
      let toolbar = this.element.find('.rich-text__toolbar')[0];
      this.viewModel.initEditor(wysiwyg, toolbar);
    },
    removed() {
      let editor = this.viewModel.attr('editor');

      if (editor) {
        editor.off('text-change');
        editor.off('selection-change');
      }
    }
  }
});
