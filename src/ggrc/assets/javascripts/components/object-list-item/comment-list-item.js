/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/object-list-item/comment-list-item.mustache');
  var tag = 'comment-list-item';
  /**
   * Simple component to show Comment Objects
   */
  can.Component.extend({
    tag: tag,
    template: tpl,
    viewModel: {
      instance: {},
      define: {
        showIcon: {
          type: Boolean,
          value: false
        },
        iconCls: {
          get: function () {
            return this.attr('showIcon') ?
            'fa-' + this.attr('itemData.title').toLowerCase() :
            '';
          }
        },
        itemData: {
          get: function () {
            return this.attr('instance');
          }
        },
        itemText: {
          get: function () {
            return this.attr('itemData.description');
          }
        },
        hasRevision: {

        },

      }
    }
  });
})(window.can, window.GGRC);
