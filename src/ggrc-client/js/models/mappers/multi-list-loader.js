/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import Mappings from './mappings';

(function (GGRC, can) {
  GGRC.ListLoaders.MultiListLoader =
    GGRC.ListLoaders.BaseListLoader.extend({}, {
      init: function (sources) {
        this._super();

        this.sources = sources || [];
      },
      init_listeners: function (binding) {
        let self = this;

        if (!binding.source_bindings) {
          binding.source_bindings = [];
        }

        _.forEach(this.sources, function (source) {
          let sourceBinding = Mappings.getBinding(source, binding.instance);
          if (source) {
            binding.source_bindings.push(sourceBinding);
            self.init_source_listeners(binding, sourceBinding);
          }
        });
      },
      insert_from_source_binding: function (binding, results, index) {
        let newResults;

        newResults = _.filteredMap(results,
          (result) => this.make_result(result.instance, [result], binding));
        this.insert_results(binding, newResults);
      },
      init_source_listeners: function (binding, sourceBinding) {
        let self = this;

        self.insert_from_source_binding(binding, sourceBinding.list);

        sourceBinding.list.bind('add', function (ev, results) {
          self.insert_from_source_binding(binding, results);
        });

        sourceBinding.list.bind('remove', function (ev, results) {
          _.forEach(results, function (result) {
            self.remove_instance(binding, result.instance, result);
          });
        });
      },
      _refresh_stubs: function (binding) {
        let deferreds = [];

        _.forEach(binding.source_bindings, function (sourceBinding) {
          deferreds.push(sourceBinding.refresh_stubs());
        });

        return $.when(...deferreds);
      },
    });
})(window.GGRC, window.can);
