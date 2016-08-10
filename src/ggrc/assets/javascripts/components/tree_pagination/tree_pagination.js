/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

/**
 * A component that renders a tree pagination widget
 * Usage: <tree-pagination paging="paging"></tree-pagination>
 */
(function (GGRC, can) {
  GGRC.Components('treePagination', {
    tag: 'tree-pagination',
    template: can.view(
      GGRC.mustache_path +
      '/components/tree_pagination/tree_pagination.mustache'
    ),
    init: function () {
      /**
       * Entrance object validation
       *
       * paging = {
       *  current: {Number}, - current page number
       *  pageSize: {Number}, - amount elements on the page
       *  total: {Number}, - total amount of elements
       *  count: {Number}, - total amount of pages
       *  pageSizeSelect: {Array} - array of numbers that used for pageSize popover
       *  disabled: {Boolean} - true if frontend doesn't finish request to the server otherwise false
       * }
       */
      if (!this.scope.attr('paging')) {
        throw new Error('Paging object didn\'t init');
      }
    },
    scope: {
      /**
       * Gets value from input and after validation set it to paging.current
       * @param {Object} object - paging object
       * @param {Object} input - DOM element
       * @param {Object} event - DOM event
       */
      setCurrentPage: function (object, input, event) {
        var _value;
        var _page;
        event.stopPropagation();
        if (!this.paging.attr('disabled')) {
          _value = parseInt(input.val(), 10);
          _page = Math.min(Math.max(_value, 1) || 1, this.paging.count);

          this.paging.attr('current', _page);
        }
        input.val('');
        input.blur();
      },
      changePageSize: function (size) {
        if (!this.paging.attr('disabled')) {
          this.paging.attr('pageSize', size);
          this.paging.attr('current', 1);
        }
      },
      setLastPage: function () {
        if (this.paging.current < this.paging.count &&
          !this.paging.attr('disabled')) {
          this.paging.attr('current', this.paging.count);
        }
      },
      setFirstPage: function () {
        if (this.paging.current > 1 && !this.paging.attr('disabled')) {
          this.paging.attr('current', 1);
        }
      },
      setPrevPage: function () {
        if (this.paging.current > 1 && !this.paging.attr('disabled')) {
          this.paging.attr('current', this.paging.current - 1);
        }
      },
      setNextPage: function () {
        if (this.paging.current < this.paging.count &&
          !this.paging.attr('disabled')) {
          this.paging.attr('current', this.paging.current + 1);
        }
      }
    },
    helpers: {
      /**
       * @param {Number|String} current - current page number
       * @param {Number|String} count - total amount of pages
       * @return {string} pagination placeholder
       */
      paginationPlaceholder: function (current, count) {
        var _radix = 10;
        var _current = parseInt(Mustache.resolve(current), _radix);
        var _count = parseInt(Mustache.resolve(count), _radix);

        if (_count && _count >= _current) {
          return 'Page ' + _current + ' of ' + _count;
        } else if (!_count) {
          return '';
        }

        return 'Wrong value';
      },
      /**
       * @param {Number|String} current - current page number
       * @param {Number|String} size - amount elements on the page
       * @param {Number|String} total - total amount of elements
       * @return {string} - pagination info
       */
      paginationInfo: function (current, size, total) {
        var _radix = 10;
        var _first;
        var _last;
        var _current = parseInt(Mustache.resolve(current), _radix);
        var _size = parseInt(Mustache.resolve(size), _radix);
        var _total = parseInt(Mustache.resolve(total), _radix);

        _first = (_current - 1) * _size + 1;
        _last = _current * _size < _total ? _current * _size : _total;

        return _last ? _first + '-' + _last + ' of ' + _total + ' items' :
          'No records';
      }
    }
  });
})(window.GGRC, window.can);
