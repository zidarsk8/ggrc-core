/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  can.Component.extend({
    tag: 'paginate',
    template: can.view(GGRC.mustache_path + '/base_objects/paginate.mustache'),
    scope: {
      list: null,
      current: 0,
      perPage: '@',
      /**
        * List of currently displayed enteries
        *
        * We are slicing input list into parts and passing them to enteries
        *
        * @return {Array} - List of enteries for current page
        */
      entries: function () {
        var list = this.attr('list');
        var perPage = Number(this.attr('perPage'));
        var current = this.attr('current');

        return list.slice(current * perPage, current * perPage + perPage);
      },
      /**
        * Get list of pages
        *
        * @return {Array} - List of pagination objects
        *                   {
        *                     number: `Display page - we are adding 1 to avoid having page 0`
        *                     pageNum: `True page number that gets passed to setPage function`
        *                   }
        */
      pages: function () {
        var list = this.attr('list');
        var perPage = Number(this.attr('perPage'));
        var pages = Math.ceil(list.length / perPage);

        return new can.List(_.times(pages, function (num) {
          return {
            number: num + 1,
            pageNum: num
          };
        }));
      },
      /**
        * Set current page
        *
        * @param {Object} page - current page context
        * @param {jQuery.Object} el - clicked element
        * @param {Object} ev - click event handler
        */
      setPage: function (page, el, ev) {
        ev.preventDefault();

        this.attr('current', page.pageNum);
      }
    }
  });
})(window.can, window.can.$);
