/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  can.Construct("GGRC.ListLoaders.BaseListLoader", {
      binding_factory: function (instance, loader) {
        return new GGRC.ListLoaders.ListBinding(instance, loader);
      }
  }, {
      init: function () {
      },

      attach: function (instance) {
        var binding = this.constructor.binding_factory(instance, this);
        this.init_listeners(binding);
        return binding;
      },

      make_result: function (instance, mappings, binding) {
        return new GGRC.ListLoaders.MappingResult(instance, mappings, binding);
      },

      find_result_by_instance: function (result, list) {
        var i;
        var found_result = null;
        var old_result;

        for (i=0; !found_result && i<list.length; i++) {
          old_result = list[i];
          if (old_result.instance.id == result.instance.id
              && old_result.instance.constructor.shortName
                  == result.instance.constructor.shortName) {
            found_result = old_result;
          }
        }

        return found_result;
      },

      is_duplicate_result: function (old_result, new_result) {
        var o = old_result
          , n = new_result
          ;

        if (o.instance === n.instance) {// && o.binding  === n.binding) {
          if (o.mappings === n.mappings) {
            return true;
          }
          o = o.mappings;
          n = n.mappings;
          if (o && n && o.length === 1 && n.length === 1) {
            o = o[0];
            n = n[0];
            if (o.binding === n.binding) {
              if (o.instance === n.instance
                  && (o.mappings.length > 0 || n.mappings.length > 0)) {
                o = o.mappings;
                n = n.mappings;
                if (o && n && o.length === 1 && n.length === 1) {
                  o = o[0];
                  n = n[0];
                }
              }

              if (o.binding === n.binding
                  && o.instance === true
                  && n.instance === true
                  && o.mappings && o.mappings.length === 0
                  && n.mappings && n.mappings.length === 0) {
                return true;
              }
            }
          }
        }

        return false;
      },

      insert_results: function (binding, results) {
        var self = this
          , all_binding_results = []
          , new_instance_results = []
          , instances_to_refresh = []
          ;

        can.each(results, function (new_result) {
          var found_result = null;
          var mapping_attr;

          found_result = self.find_result_by_instance(new_result, binding.list);

          if (!found_result && binding.pending_list) {
            found_result = self.find_result_by_instance(new_result, binding.pending_list);
          }

          if (!found_result) {
            found_result = self.find_result_by_instance(new_result, new_instance_results);
          }

          if (found_result) {
            if (self.is_duplicate_result(found_result, new_result)) {
              return;
            }

            mapping_attr = found_result.mappings;
            // Since we're adding the result as its own mapping, use
            // new_result as the mapping instead of new_result.mappings?

            can.each(new_result.mappings, function (mapping) {
              // TODO: Examine when this will be false -- is it a sign of
              //   duplicate work?
              if (mapping_attr.indexOf && mapping_attr.indexOf(mapping) === -1) {
                found_result.insert_mapping(mapping);
                instances_to_refresh.push(new_result.instance);
              }
            });

            all_binding_results.push(found_result);
          } else {
            //  FIXME: Loaders should be passing in newly instantiated results,
            //    so this line should be:
            //      found_result = new_result;
            //    but it's not a big deal
            found_result = self.make_result(new_result.instance, new_result.mappings, binding);
            new_instance_results.push(found_result);
            instances_to_refresh.push(new_result.instance);
            // FIXME: Also queue mappings to refresh?

            all_binding_results.push(found_result);
          }
        });

        if (new_instance_results.length > 0) {
          binding.list.push.apply(binding.list, new_instance_results);

          //  TODO: Examine whether deferring this list insertion avoids
          //    causing client-side freezes
          /*if (!binding.pending_list)
            binding.pending_list = [];
          binding.pending_list.push.apply(binding.pending_list, new_instance_results);

          if (!binding.pending_timeout) {
            binding.pending_deferred = new $.Deferred();
            binding.pending_timeout = setTimeout(function() {
              binding.list.push.apply(binding.list, binding.pending_list);
              delete binding.pending_list;
              delete binding.pending_timeout;
              binding.pending_deferred.resolve();
              delete binding.pending_deferred;
            }, 100);
          }*/
        }

        return all_binding_results;
      },

      remove_instance: function (binding, instance, mappings) {
        var indexes_to_remove = [];

        if (!(can.isArray(mappings) || mappings instanceof can.Observe.List))
          mappings = [mappings];

        can.each(binding.list, function (data, instance_index) {
          var mapping_attr = binding.list[instance_index].mappings;

          if (data.instance.id == instance.id
              && data.instance.constructor.shortName == instance.constructor.shortName) {
            if (mapping_attr.length == 0) {
              indexes_to_remove.push(instance_index);
            } else {
              can.each(mappings, function (mapping) {
                var was_removed = data.remove_mapping(mapping);
                if (was_removed) {
                  if (mapping_attr.length == 0)
                    indexes_to_remove.push(instance_index);
                }
              });
            }
          }
        });
        can.each(indexes_to_remove.sort(), function (index_to_remove, count) {
          binding.list.splice(index_to_remove - count, 1);
        });
      },

      refresh_stubs: function (binding) {
        if (!binding._refresh_stubs_deferred) {
          binding._refresh_stubs_deferred = $.when(this._refresh_stubs(binding));
        }
        return binding._refresh_stubs_deferred
          .then(function () { return binding.list; });
      },

      refresh_instances: function (binding, force) {
        if (force || !binding._refresh_instances_deferred) {
          binding._refresh_instances_deferred =
            $.when(this._refresh_instances(binding, force));
        }
        return binding._refresh_instances_deferred
          .then(
            function () { return binding.list; },
            function () {
              setTimeout(function () {
                delete binding._refresh_instances_deferred;
              }, 10);
              return this;
            });
      },

      _refresh_instances: function (binding, force) {
        return this.refresh_stubs(binding)
          .then(function () {
            var refresh_queue = new RefreshQueue();
            can.each(binding.list, function (result) {
              refresh_queue.enqueue(result.instance, force);
            });
            return refresh_queue.trigger();
          });
      }
  });
})(window.GGRC, window.can);
