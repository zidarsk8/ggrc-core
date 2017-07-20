/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/sub-tree-models.mustache';

(function (can, GGRC) {
  'use strict';

  var viewModel = can.Map.extend({
    define: {
      isActive: {
        type: Boolean,
        value: false
      }
    },
    modelsList: null,
    title: null,
    $el: null,
    activate: function () {
      this.attr('isActive', true);
    },
    setDisplayModels: function (ev) {
      var selectedModels = this.attr('modelsList').filter(function (item) {
        return item.display;
      }).map(function (item) {
        return item.name;
      });
      can.trigger(this.attr('$el'), 'childModelsChange', [selectedModels]);
      this.attr('isActive', false);
      ev.stopPropagation();
    },
    selectAll: function (ev) {
      ev.stopPropagation();
      this.attr('modelsList').forEach(function (item) {
        item.attr('display', true);
      });
    },
    selectNone: function (ev) {
      ev.stopPropagation();
      this.attr('modelsList').forEach(function (item) {
        item.attr('display', false);
      });
    }
  });

  GGRC.Components('subTreeModels', {
    tag: 'sub-tree-models',
    template: template,
    viewModel: viewModel,
    events: {
      inserted: function () {
        this.viewModel.attr('$el', this.element);
      },
      '.sub-tree-models mouseleave': function () {
        this.viewModel.attr('isActive', false);
      }
    }
  });
})(window.can, window.GGRC);
