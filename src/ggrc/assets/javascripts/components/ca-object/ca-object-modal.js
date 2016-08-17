/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/ca-object/ca-object-modal.mustache');
  var baseCls = 'attachment-modal';

  function recalculatePosition(el) {
    var pos = el[0].getBoundingClientRect();
    var top = Math
      .floor(window.document.body.scrollHeight / 2 - pos.height / 2);
    var left = Math
      .floor(window.document.body.scrollWidth / 2 - pos.width / 2);

    return {top: top, left: left};
  }

  GGRC.Components('customAttributeObjectModal', {
    tag: 'ca-object-modal',
    template: tpl,
    scope: {
      instance: null,
      modifiedField: null,
      modalCls: '',
      modalOverlayCls: '',
      modalEl: null,
      isPerson: false,
      comment: false,
      evidence: false,
      state: {
        open: false,
        save: false,
        empty: false,
        controls: false
      },
      applyState: function () {
        this.toggle(this.attr('state.open'));
      },
      saveAttachments: function () {
        this.attr('state.save', true);
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
        var modal;
        var isPerson =
          this.attr('modifiedField.value') &&
          this.attr('modifiedField.type') === 'person';

        this.setAttachmentFields(isOpen);
        this.attr('modalCls', isOpen ? baseCls + '-open' : '');
        this.attr('modalOverlayCls', isOpen ? baseCls + '__overlay-open' : '');
        this.attr('isPerson', isPerson);
        if (isOpen && this.attr('modalEl')) {
          modal = this.attr('modalEl');
          modal.offset(recalculatePosition(modal));
        }

        if (this.attr('comment')) {
          this.attr('state.empty', true);
        }
      },
      setAttachmentFields: function (isOpen) {
        var attachments = this.attr('modifiedField.fields');

        if (attachments && attachments.length) {
          attachments.forEach(function (item) {
            this.attr(item, isOpen);
          }.bind(this));
        }
      },
      mapToInternal: function () {
        this.attr('modifiedField', this.attr('modal'));
      }
    },
    events: {
      inserted: function (el) {
        var modal = el.find('.' + baseCls);
        modal.appendTo('body');
        this.scope.attr('modalEl', modal);
        el.find('.' + baseCls + '__overlay').appendTo('body');
      },
      show: function (scope, ev, val) {
        if (val) {
          this.scope.mapToInternal();
          this.scope.show();
        }
      },
      '{scope.modal} open': 'show',
      '{scope.state} open': function () {
        this.scope.applyState();
      }
    }
  });
})(window.can, window.GGRC);
