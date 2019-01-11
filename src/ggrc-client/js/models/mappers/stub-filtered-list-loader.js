/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import Mappings from './mappings';

(function (GGRC, can) {
  GGRC.ListLoaders.BaseListLoader('GGRC.ListLoaders.StubFilteredListLoader', {},
    {
      init: function (source, filterFn) {
        this._super();

        this.source = source;
        this.filter_fn = filterFn;
      },
      init_listeners: function (binding) {
        let self = this;
        let matchingResults;

        if (typeof this.source === 'string') {
          binding.source_binding = Mappings.get_binding(
            this.source,
            binding.instance);
        } else {
          binding.source_binding = this.source;
        }
        binding.source_binding.list.bind('add', function (ev, results) {
          if (binding._refresh_stubs_deferred &&
            binding._refresh_stubs_deferred.state() !== 'pending') {
            matchingResults = can.map(can.makeArray(results), function (res) {
              if (self.filter_fn(res)) {
                return self.make_result(res.instance, [res], binding);
              }
            });
            self.insert_results(binding, matchingResults);
          }
        });

        binding.source_binding.list.bind('remove', function (ev, results) {
          _.forEach(results, function (result) {
            self.remove_instance(binding, result.instance, result);
          });
        });
      },
      _refresh_stubs: function (binding) {
        return binding.source_binding.refresh_stubs()
          .then(function (results) {
            let matchingResults = can.map(can.makeArray(results),
              function (result) {
                if (this.filter_fn(result)) {
                  return this.make_result(result.instance, [result], binding);
                }
              }.bind(this));
            this.insert_results(binding, matchingResults);
          }.bind(this));
      },
    });
})(window.GGRC, window.can);
