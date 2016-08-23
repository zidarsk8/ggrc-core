/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.StubFilteredListLoader", {
  }, {
      init: function (source, filter_fn) {
        this._super();

        this.source = source;
        this.filter_fn = filter_fn;
      }

    , init_listeners: function (binding) {
        var self = this;

        if (typeof this.source === "string") {
          binding.source_binding = binding.instance.get_binding(this.source);
        } else {
          binding.source_binding = this.source;
        }
        binding.source_binding.list.bind("add", function (ev, results) {
          if (binding._refresh_stubs_deferred && binding._refresh_stubs_deferred.state() !== "pending") {
            var matching_results = can.map(can.makeArray(results), function (result) {
              if (self.filter_fn(result)) {
                return self.make_result(result.instance, [result], binding);
              }
            });
            self.insert_results(binding, matching_results);
          }
        });

        binding.source_binding.list.bind("remove", function (ev, results) {
          can.each(results, function (result) {
            self.remove_instance(binding, result.instance, result);
          });
        });
      }

    , _refresh_stubs: function (binding) {
        return binding.source_binding.refresh_stubs()
          .then(function (results) {
            var matching_results = can.map(can.makeArray(results), function (result) {
                  if (this.filter_fn(result)) {
                    return this.make_result(result.instance, [result], binding);
                  }
                }.bind(this));
            this.insert_results(binding, matching_results);
          }.bind(this));
      }
  });
})(window.GGRC, window.can);
