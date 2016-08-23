/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/mapped-objects/mapped-objects-list.mustache');
  var tag = 'assessment-mapped-objects-list';
  var baseCls = '.assessment-mapped-objects';
  var popoverCls = baseCls + '__popover';
  var itemTplsBasePath = GGRC.mustache_path +
      '/components/assessment/mapped-objects/item-templates/';
  /**
   * Assessment specific mapped objects view component
   */
  GGRC.Components('assessmentMappedObjectsList', {
    tag: tag,
    template: tpl,
    scope: {
      selectedItem: null,
      selectedEl: null,
      itemsTpl: null,
      items: [],
      getComputedItemsTpl: function (tpl) {
        return itemTplsBasePath + tpl + '.mustache';
      },
      addSelection: function (ctx, el) {
        this.removeSelection();
        this.attr('selectedEl', el);
        this.attr('selectedItem', ctx.instance);
        ctx.instance.attr('isSelected', true);
      },
      removeSelection: function () {
        this.attr('selectedItem', null);
        this.attr('selectedEl', null);
        this.items.forEach(function (obj) {
          obj.instance.attr('isSelected', false);
        });
      }
    },
    helpers: {
      renderItemsTpl: function (options) {
        var tpl = this.attr('itemsTpl');
        tpl = this.getComputedItemsTpl(tpl);
        return can.view.render(tpl, options.scope);
      }
    },
    events: {
      '{window} click': function (el, ev) {
        var popover = this.element.find(popoverCls);

        var isClickInsidePopover = popover.has(ev.target).length ||
          popover.is(ev.target);

        var isClickedInsideContent = this.element.has(ev.target).length ||
          this.element.is(ev.target);

        if (!isClickedInsideContent && !isClickInsidePopover) {
          this.scope.removeSelection();
        }
      }
    }
  });
})(window.can, window.GGRC);
