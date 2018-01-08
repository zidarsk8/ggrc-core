/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  GGRC.ListLoaders.BaseListLoader('GGRC.ListLoaders.FirstElementLoader', {}, {
    init_listeners: function (binding) {
      var self = this;

      binding.source_binding = binding.instance.get_binding(this.source);

      binding.source_binding.list.bind('add', function (ev, results) {
        var matchingResults = results[0];
        if (self.list.length < 1)
          self.insert_results(binding, [matchingResults]);
      });

      binding.source_binding.list.bind('remove', function (ev, results) {
        can.each(results, function (result) {
          self.remove_instance(binding, result.instance, result);
        });
        if (self.list.length < 1)
          self.insert_results(binding, [binding.source_binding.list[0]]);
      });
    },
    _refresh_stubs: function (binding) {
      var self = this;

      return binding.source_binding.refresh_stubs()
        .then(function (results) {
          var matchingResults = results[0];
          self.insert_results(binding, matchingResults);
        });
    }
  });
})(window.GGRC, window.can);
