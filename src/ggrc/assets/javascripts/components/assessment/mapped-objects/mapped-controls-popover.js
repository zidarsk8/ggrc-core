/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/mapped-objects/mapped-controls-popover.mustache');
  var tag = 'assessment-mapped-controls-popover';
  /**
   * Assessment specific mapped objects popover view component
   */
  GGRC.Components('mappedControlsPopover', {
    tag: tag,
    template: tpl,
    scope: {
      item: null,
      itemData: null,
      objectives: new can.List(),
      regulations: new can.List(),
      isLoading: false,
      /**
       * Gets params for current id
       * @return {Object} params for current id
       */
      getParams: function () {
        var id = this.attr('itemData.id');
        var params = {};
        var relevant = {
          id: id,
          type: 'Control'
        };
        var fields = ['id', 'title', 'notes', 'description'];
        params.data = [
          GGRC.Utils.QueryAPI.buildParam('Objective', {}, relevant, fields),
          GGRC.Utils.QueryAPI.buildParam('Regulation', {}, relevant, fields)
        ];
        return params;
      },
      loadItems: function () {
        var params = this.getParams();
        var self = this;
        this.attr('isLoading', true);
        GGRC.Utils.QueryAPI
          .makeRequest(params)
          .done(function (responseArr) {
            var objectives;
            var regulations;
            responseArr.forEach(function (item) {
              if (item.hasOwnProperty('Objective')) {
                objectives = item.Objective.values;
              }
              if (item.hasOwnProperty('Regulation')) {
                regulations = item.Regulation.values;
              }
            });
            self.attr('objectives').replace(objectives);
            self.attr('regulations').replace(regulations);
            self.attr('isLoading', false);
          });
      },
      /**
       * Toggles objectives and regulations
       * @param {String} index Index of selected item
       */
      toggleItems: function (index) {
        if (index) {
          this.attr('itemData', this.attr('item.data'));
          this.loadItems();
        } else {
          this.attr('objectives').replace([]);
          this.attr('regulations').replace([]);
        }
      }
    },
    events: {
      '{scope.item} index': function (scope, ev, index) {
        this.scope.toggleItems(index);
      }
    }
  });
})(window.can, window.GGRC);
