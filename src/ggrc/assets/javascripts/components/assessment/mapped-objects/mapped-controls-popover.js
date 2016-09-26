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
   * Assessment specific mapped controls popover view component
   */
  var defaultResponseArr = [{
    Objective: {
      values: []
    }
  }, {
    Regulation: {
      values: []
    }
  }];

  GGRC.Components('mappedControlsPopover', {
    tag: tag,
    template: tpl,
    scope: {
      item: null,
      expanded: false,
      objectives: new can.List(),
      regulations: new can.List(),
      isLoading: false,
      getParams: function (id, type) {
        var params = {};
        var relevant = {
          id: id,
          type: type
        };
        var fields = ['id', 'title', 'notes', 'description'];
        params.data = [
          GGRC.Utils.QueryAPI.buildParam('Objective', {}, relevant, fields),
          GGRC.Utils.QueryAPI.buildParam('Regulation', {}, relevant, fields)
        ];
        return params;
      },
      setItems: function (responseArr) {
        responseArr.forEach(function (item) {
          if (item.Objective) {
            this.attr('objectives').replace(item.Objective.values);
          }
          if (item.Regulation) {
            this.attr('regulations').replace(item.Regulation.values);
          }
        }.bind(this));
      },
      loadItems: function () {
        var id = this.attr('item.data.id');
        var type = this.attr('item.data.type');
        var params;

        if (!id || !type) {
          this.setItems(defaultResponseArr);
          return;
        }
        params = this.getParams(id, type);

        this.attr('isLoading', true);

        GGRC.Utils.QueryAPI
          .makeRequest(params)
          .done(this.setItems.bind(this))
          .fail(function () {
            console.warn('Errors are: ', arguments);
            this.setItems(defaultResponseArr);
          }.bind(this))
          .always(function () {
            this.attr('isLoading', false);
          }.bind(this));
      }
    },
    events: {
      '{scope} expanded': function (scope, ev, isExpanded) {
        if (isExpanded) {
          this.scope.loadItems();
        }
      }
    }
  });
})(window.can, window.GGRC);
