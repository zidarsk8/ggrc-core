/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.CrossListLoader", {
  }, {
      init: function (local_mapping, remote_mapping) {
        this._super();

        this.local_mapping = local_mapping;
        this.remote_mapping = remote_mapping;
      }

    , init_listeners: function (binding) {
        if (!binding.bound_insert_from_source_binding) {
          binding.bound_insert_from_source_binding =
            this.proxy("insert_from_source_binding", binding);
          binding.bound_remove_from_source_binding =
            this.proxy("remove_from_source_binding", binding);
        }

        binding.source_binding = binding.instance.get_binding(this.local_mapping);

        binding.source_binding.list.bind(
            "add", binding.bound_insert_from_source_binding);
        binding.source_binding.list.bind(
            "remove", binding.bound_remove_from_source_binding);
      }

    , insert_from_source_binding: function (binding, ev, local_results, index) {
        var self = this;
        can.each(local_results, function (local_result) {
          // FIXME: This is identical to code in _refresh_stubs
          var remote_binding = self.insert_local_result(binding, local_result);
          remote_binding.refresh_instance().then(function () {
            remote_binding.refresh_stubs();
          });
        });
      }

    , remove_from_source_binding: function (binding, ev, local_results, index) {
        var self = this;
        can.each(local_results, function (local_result) {
          self.remove_local_result(binding, local_result);
        });
      }

    , insert_local_result: function (binding, local_result) {
        var self = this;
        var i;
        var local_results;
        var remote_binding;

        if (!binding.remote_bindings)
          binding.remote_bindings = [];

        for (i=0; i<binding.remote_bindings.length; i++) {
          if (binding.remote_bindings[i].instance === local_result.instance)
            return binding.remote_bindings[i];
        }

        remote_binding =
          local_result.instance.get_binding(self.remote_mapping);
        remote_binding.bound_insert_from_remote_binding =
          this.proxy("insert_from_remote_binding", binding, remote_binding);
        remote_binding.bound_remove_from_remote_binding =
          this.proxy("remove_from_remote_binding", binding, remote_binding);

        binding.remote_bindings.push(remote_binding);

        remote_binding.list.bind(
          "add", remote_binding.bound_insert_from_remote_binding);
        remote_binding.list.bind(
          "remove", remote_binding.bound_remove_from_remote_binding);

        local_results = can.map(remote_binding.list, function (result) {
          return self.make_result(result.instance, [result], binding);
        });
        self.insert_results(binding, local_results);

        return remote_binding;
      }

    , remove_local_result: function (binding, local_result) {
        var self = this
          , remote_binding
          , i
          , found = false
          , remote_binding_index
          ;

        if (!binding.remote_bindings)
          binding.remote_bindings = [];

        for (i=0; i<binding.remote_bindings.length; i++) {
          if (binding.remote_bindings[i].instance === local_result.instance)
            remote_binding = binding.remote_bindings[i];
        }

        if (!remote_binding) {
          console.debug("Removed binding not found:", local_result, binding);
          return;
        }

        remote_binding.list.unbind(
            "add", remote_binding.bound_insert_from_remote_binding);
        remote_binding.list.unbind(
            "remove", remote_binding.bound_remove_from_remote_binding);

        can.each(remote_binding.list, function (result) {
          self.remove_instance(binding, result.instance, result);
        });

        remote_binding_index = binding.remote_bindings.indexOf(remote_binding);
        binding.remote_bindings.splice(remote_binding_index, 1);
      }

    , insert_from_remote_binding: function (binding, remote_binding, ev, results, index) {
        var self = this;
        var new_results = can.map(results, function (result) {
          return self.make_result(result.instance, [result], binding);
        });
        this.insert_results(binding, new_results);
      }

    , remove_from_remote_binding: function (binding, remote_binding, ev, results, index) {
        var self = this;
        can.each(results, function (result) {
          self.remove_instance(binding, result.instance, result);
        });
      }

    , _refresh_stubs: function (binding) {
        var self = this;

        return binding.source_binding.refresh_stubs().then(function (local_results) {
          var deferreds = [];

          can.each(local_results, function (local_result) {
            var remote_binding = self.insert_local_result(binding, local_result)
              , deferred = remote_binding.refresh_instance().then(function () {
                  return remote_binding.refresh_stubs();
                })
              ;

            deferreds.push(deferred);
          });

          return $.when.apply($, deferreds);
        })
        .then(function () { return binding.list; });
      }
  });
})(window.GGRC, window.can);
