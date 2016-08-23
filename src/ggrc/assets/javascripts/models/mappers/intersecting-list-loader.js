/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.IntersectingListLoader", {
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
          var source_binding = null;
          /// Here is a deviation from the norm, since we want to
          ///  allow source bindings from possibly several disparate
          ///  instances.  Pass them in as already created objects
          ///  and we won't try to find them on the binding instance.
          if(typeof source === "string") {
            source_binding = binding.instance.get_binding(source);
          } else {
            source_binding = source;
          }
          if (source) {
            binding.source_bindings.push(source_binding);
          }
        });
        self.init_source_listeners(binding, binding.source_bindings);
      }

    , insert_from_source_binding: function (binding, results, index) {
        var self = this
          , new_results
          , lists = can.map(
            binding.source_bindings,
            function (source) {
              return [can.map(
                source.list,
                function (result) {
                  return result.instance;
                })];
              })
          ;

        new_results = can.map(results, function (result) {
          // only the results that have membership in all lists will be added.
          if (can.reduce(lists, function (found, list) {
            return found && !!~can.inArray(result.instance, list);
          }, true)) {
            return self.make_result(result.instance, [result], binding);
          }
        });
        self.insert_results(binding, new_results);
      }

    , init_source_listeners: function (binding, source_bindings) {
        var self = this;

        can.each(source_bindings, function (source_binding) {

          self.insert_from_source_binding(binding, source_binding.list);

          source_binding.list.bind("add", function (ev, results) {
            self.insert_from_source_binding(binding, results);
          });

          source_binding.list.bind("remove", function (ev, results) {
            can.each(results, function (result) {
              self.remove_instance(binding, result.instance, result);
            });
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
