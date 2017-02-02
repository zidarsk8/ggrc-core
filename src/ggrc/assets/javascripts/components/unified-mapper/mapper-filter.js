/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC) {
  'use strict';

  can.Component.extend('mapperFilter', {
    tag: 'mapper-filter',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-filter.mustache'
    ),
    viewModel: {
      filter: '',
      isExpression: false,
      checkExpression: function () {
        var currentFilter = GGRC.query_parser.parse(this.attr('filter'));
        var isExpression =
          !!currentFilter && !!currentFilter.expression.op &&
          currentFilter.expression.op.name !== 'text_search' &&
          currentFilter.expression.op.name !== 'exclude_text_search';
        this.attr('isExpression', isExpression);
      },
      onSubmit: function () {
        this.dispatch('submit');
      },
      reset: function () {
        this.attr('filter', '');
      }
    },
    events: {
      '#mapper-filter input': function (el) {
        this.viewModel.attr('filter', el.val());
      },
      '{viewModel} filter': function () {
        this.viewModel.checkExpression();
      }
    }
  });
})(window.can, window.GGRC);
