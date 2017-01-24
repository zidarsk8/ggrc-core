/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/ca-object/ca-object-modal.mustache');
  var baseCls = 'simple-modal';

  function recalculatePosition(el) {
    var pos = el[0].getBoundingClientRect();
    var top = Math
      .floor(window.document.body.scrollHeight / 2 - pos.height / 2);
    var left = Math
      .floor(window.document.body.scrollWidth / 2 - pos.width / 2);

    return {top: top, left: left};
  }

  can.Component.extend({
    tag: 'ca-object-modal',
    template: tpl,
    viewModel: {
      define: {
        modifiedField: {
          get: function () {
            return this.attr('modal');
          }
        },
        modalCls: {
          get: function () {
            return this.attr('state.open') ? baseCls + '-open' : '';
          }
        },
        modalOverlayCls: {
          get: function () {
            return this.attr('state.open') ? baseCls + '__overlay-open' : '';
          }
        },
        state: {
          value: {
            open: false,
            save: false,
            controls: false
          }
        },
        isPerson: {
          get: function () {
            return this.attr('modifiedField.value') &&
              this.attr('modifiedField.type') === 'person';
          }
        },
        actionBtnText: {
          get: function () {
            return this.attr('comment') ? 'Save' : 'Done';
          }
        }
      },
      instance: null,
      modalEl: null,
      isEmpty: true,
      comment: false,
      evidence: false,
      saveAttachments: function () {
        return this.attr('comment') ?
          this.attr('state.save', true) :
          this.attr('state.open', false);
      },
      hide: function hide() {
        this.attr('state.open', false);
        this.attr('state.save', false);
      },
      show: function () {
        this.attr('state.open', true);
        this.attr('state.save', false);
      },
      toggle: function (isOpen) {
        this.setAttachmentFields(isOpen);
        this.setPosition(isOpen);
      },
      setAttachmentFields: function (isOpen) {
        var attachments = this.attr('modifiedField.fields');

        if (attachments && attachments.length) {
          attachments.forEach(function (item) {
            this.attr(item, isOpen);
          }.bind(this));
        }
      },
      setPosition: function (isOpen) {
        var modal = this.attr('modalEl');
        if (isOpen && modal) {
          modal.offset(recalculatePosition(modal));
        }
      }
    },
    events: {
      inserted: function (el) {
        var modal = el.find('.' + baseCls);
        modal.appendTo('body');
        this.viewModel.attr('modalEl', modal);
        el.find('.' + baseCls + '__overlay').appendTo('body');
      },
      show: function (viewModel, ev, val) {
        if (val) {
          this.viewModel.show();
        }
      },
      '{viewModel.modal} open': 'show',
      '{viewModel.state} open': function (viewModel, ev, val) {
        this.viewModel.toggle(val);
      },
      '{window} resize': function () {
        var isOpen = this.viewModel.attr('modifiedField.open');
        this.viewModel.setPosition(isOpen);
      }
    }
  });
})(window.can, window.GGRC);
