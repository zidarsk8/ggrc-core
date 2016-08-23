/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.MultiListLoader", {
  }, {
      init: function (sources) {
        this._super();

        this.sources = sources || [];
      }

    , init_listeners: function (binding) {
        var self = this;

        if (!binding.source_bindings)
          binding.source_bindings = [];

        can.each(this.sources, function (source) {
          var source_binding = binding.instance.get_binding(source);
          if (source) {
            binding.source_bindings.push(source_binding);
            self.init_source_listeners(binding, source_binding);
          }
        });
      }

    , insert_from_source_binding: function (binding, results, index) {
        var self = this
          , new_results
          ;

        new_results = can.map(results, function (result) {
          return self.make_result(result.instance, [result], binding);
        });
        self.insert_results(binding, new_results);
      }

    , init_source_listeners: function (binding, source_binding) {
        var self = this;

        self.insert_from_source_binding(binding, source_binding.list);

        source_binding.list.bind("add", function (ev, results) {
          self.insert_from_source_binding(binding, results);
        });

        source_binding.list.bind("remove", function (ev, results) {
          can.each(results, function (result) {
            self.remove_instance(binding, result.instance, result);
          });
        });
      }

    , _refresh_stubs: function (binding) {
        var deferreds = [];

        can.each(binding.source_bindings, function (source_binding) {
          deferreds.push(source_binding.refresh_stubs());
        });

        return $.when.apply($, deferreds);
      }
  });
})(window.GGRC, window.can);
