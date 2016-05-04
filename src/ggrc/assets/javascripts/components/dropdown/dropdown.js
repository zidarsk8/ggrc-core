/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  'use strict';

  /*
    Component abstracts <select> dropdown in HTML.

    It recieves `name` of the attribute that should be set and `optionsList`
    with titles and values
   */
  GGRC.Components('dropdown', {
    tag: 'dropdown',
    template: can.view(
      GGRC.mustache_path +
      '/components/dropdown/dropdown.mustache'
    ),
    scope: {
      name: '@',
      className: '@',
      onChange: $.noop,
      noValue: '@',
      /*
        Options list should be an `array` of object containing `title` and `value`
        [{
          title: `title`
          value: `value`
        }]
       */
      optionsList: null,
      options: function () {
        var none = [{
          title: 'None',
          value: ''
        }];
        var list = can.map(this.attr('optionsList'), function (option) {
          if (_.isString(option)) {
            return {
              value: option,
              title: option
            };
          }
          return option;
        });
        if (this.attr('noValue')) {
          return none.concat(list);
        }
        return list;
      }
    }
  });
})(window.can, window.can.$);
