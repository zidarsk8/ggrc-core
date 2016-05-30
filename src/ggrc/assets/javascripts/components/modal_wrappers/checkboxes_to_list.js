/*!
    Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function (can, $) {
  'use strict';

  GGRC.Components('checkboxToList', {
    tag: 'checkbox-to-list',
    template: '<content></content>',
    scope: {
      property: '@',
      instance: null,
      values: {}
    },
    init: function () {
      var scope = this.scope;
      var values = scope.attr('instance.' + scope.attr('property'));

      if (values && _.isString(values)) {
        _.each(_.splitTrim(values, ','), function (val) {
          if (val) {
            scope.attr('values.' + val, true);
          }
        });
      }
    },
    events: {
      '{scope.values} change': function () {
        var scope = this.scope;
        var values = _.getExistingKeys(scope.attr('values').serialize());
        scope.instance.attr(scope.attr('property'), values.join(','));
      }
    }
  });
})(window.can, window.can.$);
