/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  GGRC.Components('objectSearch', {
    tag: 'object-search',
    template: can.view(GGRC.mustache_path +
      '/components/object-search/object-search.mustache'),
    scope: function (attrs, parentScope, el) {
      var data = {
        search_only: true,
        object: 'MultitypeSearch',
        type: 'Program'
      };

      return {
        isLoadingOrSaving: function () {
          return this.attr('mapper.is_loading');
        },
        mapper: new GGRC.Models.MapperModel(data)
      };
    },

    events: {
      inserted: function () {
        this.setModel();
        this.scope.attr('mapper').afterShown();
      },
      setModel: function () {
        var type = this.scope.attr('mapper.type');

        this.scope.attr(
          'mapper.model', this.scope.mapper.modelFromType(type));
      },
      '{mapper} type': function () {
        var mapper = this.scope.attr('mapper');
        mapper.attr('filter', '');
        mapper.attr('afterSearch', false);
        mapper.attr('relevant').replace([]);
        this.setModel();
        setTimeout(mapper.onSubmit.bind(mapper));
      }
    }
  });
})(window.can, window.can.$);
