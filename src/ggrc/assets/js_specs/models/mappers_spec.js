

describe("working tests", function () {
    it("will have to update to jasmine 2.0 ways", function () {});
});


xdescribe("mappers", function() {
  
  var LL;
  beforeEach(function() {
    LL = GGRC.ListLoaders;
    if(!GGRC.Jasmine || !GGRC.Jasmine.MockModel) {
      can.Model.Cacheable("GGRC.Jasmine.MockModel", {}, {});
    }
  });

  describe("ListBinding", function() {});

  describe("MappingResult", function() {

    describe("#init", function() {

      it("sets the named properties to the positional parameters", function() {
        var mr;
        spyOn(LL.MappingResult.prototype, "_make_mappings").andCallFake(function(mapping_name) {
          expect(mapping_name).toBe("mappings");
          return "_mapping";
        });
        mr = new LL.MappingResult("instance", "mappings", "binding");

        expect(mr.instance).toBe("instance");
        expect(mr.binding).toBe("binding");
        expect(mr.mappings).toBe("_mapping");
        expect(LL.MappingResult.prototype._make_mappings).toHaveBeenCalledWith("mappings");
      });

      it("sets the named properties to the object properties if called with an object", function() {
        var mr;
        spyOn(LL.MappingResult.prototype, "_make_mappings").andCallFake(function(mapping_name) {
          expect(mapping_name).toBe("mappings");
          return "_mapping";
        });
        mr = new LL.MappingResult({instance: "instance", mappings: "mappings", binding: "binding"});

        expect(mr.instance).toBe("instance");
        expect(mr.binding).toBe("binding");
        expect(mr.mappings).toBe("_mapping");
        expect(LL.MappingResult.prototype._make_mappings).toHaveBeenCalledWith("mappings");
      });

    });

    describe("#_make_mappings", function() {
      it("converts all elements of the supplied array to mapping results", function() {
        var mr = new LL.MappingResult("foo", ["bar"], "baz");
        expect(mr._make_mappings(["baz", "quux", mr]))
          .toEqual([
            jasmine.any(LL.MappingResult),
            jasmine.any(LL.MappingResult),
            mr
          ]);
      });
    });
/*
    //  `get_bindings`, `bindings_compute`, `get_bindings_compute`
    //  - Returns a list of the `ListBinding` instances which are the source
    //    of "first-level mappings".
    , get_bindings: function() {
        var self = this
          , bindings = []
          ;

        this.walk_instances(function(instance, result, depth) {
          if (depth === 1)
            bindings.push(result.binding);
        });
        return bindings;
      }

    , bindings_compute: function() {
        if (!this._bindings_compute)
          this._bindings_compute = this.get_bindings_compute();
        return this._bindings_compute;
      }

    , get_bindings_compute: function() {
        var self = this;

        return can.compute(function() {
          // Unnecessarily access observe_trigger to be able to trigger change
          self.watch_observe_trigger();
          return self.get_bindings();
        });
      }

    //  `get_mappings`, `mappings_compute`, and `get_mappings_compute`
    //  - Returns a list of first-level mapping instances, even if they're
    //    several levels down due to virtual mappers like Multi or Cross
    //  - "First-level mappings" are the objects whose existence causes the
    //    `binding.instance` to be in the current `binding.list`.  (E.g.,
    //    if any of the "first-level mappings" exist, the instance will
    //    appear in the list.
    , get_mappings: function() {
        var self = this
          , mappings = []
          ;

        this.walk_instances(function(instance, result, depth) {
          if (depth == 1) {
            if (instance === true)
              mappings.push(self.instance);
            else
              mappings.push(instance);
          }
        });
        return mappings;
      }

    , mappings_compute: function() {
        if (!this._mappings_compute)
          this._mappings_compute = this.get_mappings_compute();
        return this._mappings_compute;
      }

    , get_mappings_compute: function() {
        var self = this;

        return can.compute(function() {
          // Unnecessarily access _observe_trigger to be able to trigger change
          self.watch_observe_trigger();
          return self.get_mappings();
        });
      }

    //  `walk_instances`
    //  - `binding.mappings` can have several "virtual" levels due to mappers
    //    like `Multi`, `Cross`, and `Filter` -- e.g., mappers which just
    //    aggregate or filter results of other mappers.  `walk_instances`
    //    iterates over these "virtual" levels to emit instances only once
    //    per time they appear in a traversal path of `binding.mappings`.
    , walk_instances: function(fn, last_instance, depth) {
        var i;
        if (depth == null)
          depth = 0;
        if (this.instance !== last_instance) {
          fn(this.instance, this, depth);
          depth++;
        }
        for (i=0; i<this.mappings.length; i++) {
          this.mappings[i].walk_instances(fn, this.instance, depth);
        }
      }
*/

  });

  describe("GGRC.ListLoaders.BaseListLoader", function() {

    var ll;
    beforeEach(function() {
      ll = new GGRC.ListLoaders.BaseListLoader();
      //init_listeners is abstract -- called by base init but not implemented in base.
      ll.init_listeners = jasmine.createSpy();
    });

    describe("#attach", function() {

      it("calls the binding factory for the type", function() {
        spyOn(GGRC.ListLoaders.BaseListLoader, "binding_factory");

        ll.attach("instance");
        expect(GGRC.ListLoaders.BaseListLoader.binding_factory).toHaveBeenCalledWith("instance", ll);
      });

      it("inits the listeners", function() {
        var fake_binding = {};
        spyOn(GGRC.ListLoaders.BaseListLoader, "binding_factory").andReturn(fake_binding);

        ll.attach("instance");
        expect(ll.init_listeners).toHaveBeenCalledWith(fake_binding);
      });

    });

    describe("#find_result_by_instance", function() {

      var not_found, found, list;
      beforeEach(function() {
        not_found = new GGRC.Jasmine.MockModel({ id : 1 });
        found = new GGRC.Jasmine.MockModel({ id : 2 });
        list = [{instance : found }];
      });

      it("returns null if no result", function() {
        expect(ll.find_result_by_instance({ instance : not_found }, list)).toBe(null);
      });

      it("returns the result if found", function() {
        expect(ll.find_result_by_instance({ instance : found }, list)).toBe(list[0]);
      });

    });

    describe("#is_duplicate_result", function() {

      it("returns false if instances do not match", function() {
        expect(ll.is_duplicate_result({instance : 1}, {instance : 2 })).toBe(false);
      });

      it("returns true if instances AND mappings match", function() {
        expect(ll.is_duplicate_result({instance : 1, mappings : 'a'}, {instance : 1, mappings : 'a' })).toBe(true);
      });

      it("returns false if either result has empty mappings", function() {
        expect(ll.is_duplicate_result({instance : 1, mappings : null}, {instance : 1, mappings : [] })).toBe(false);
        expect(ll.is_duplicate_result({instance : 1, mappings : []}, {instance : 1, mappings : null })).toBe(false);
        expect(ll.is_duplicate_result({instance : 1, mappings : []}, {instance : 1, mappings : [] })).toBe(false);
        //expect(ll.is_duplicate_result({instance : 1, mappings : 'a'}, {instance : 1, mappings : [] })).toBe(false);
      });

      it("returns false if either result has multiple mappings", function() {
        expect(ll.is_duplicate_result({instance : 1, mappings : ['a', 'b']}, {instance : 1, mappings : ['a'] })).toBe(false);
        expect(ll.is_duplicate_result({instance : 1, mappings : ['a']}, {instance : 1, mappings : ['a','b'] })).toBe(false);
        expect(ll.is_duplicate_result({instance : 1, mappings : ['a','b']}, {instance : 1, mappings : ['a','b'] })).toBe(false);
        //expect(ll.is_duplicate_result({instance : 1, mappings : 'a'}, {instance : 1, mappings : [] })).toBe(false);
      });

      it("returns true if boths results have null mappings", function() {
        expect(ll.is_duplicate_result({instance : 1, mappings : null }, {instance : 1, mappings : null })).toBe(true);
      });

      it("returns true if both results have one non-matching mapping with no dependent mapping (instance === true)", function() {
        expect(ll.is_duplicate_result(
          {instance : 1, mappings : [{instance : true, mappings : [], binding : 2 }], binding : 1 },
          {instance : 1, mappings : [{instance : true, mappings : [], binding : 2 }], binding : 1 }
        )).toBe(true);
      });

    });

    describe("#insert_results", function() {

      var binding, fake_find_result;
      beforeEach(function() {
        fake_find_result = { mappings : [] };
        spyOn(ll, "find_result_by_instance");
        spyOn(ll, "is_duplicate_result");
        spyOn(ll, "make_result").andReturn(fake_find_result);
        binding = { list : [] };
      });

      it("returns an empty list, and pushes nothing to binding, if no results", function() {
        var ret = ll.insert_results(binding, []);
        expect(ret).toEqual([]);
        expect(binding.list).toEqual([]);
      });


      it("returns a list with inserted bindings, if results", function() {
        var ret = ll.insert_results(binding, ['a']);
        expect(ret).toEqual([fake_find_result]);
        expect(binding.list).toEqual([fake_find_result]);
      });

      it("returns an empty list, and pushes nothing to binding, if results are duplicates", function() {
        var ret;
        ll.find_result_by_instance.andReturn(fake_find_result);
        ll.is_duplicate_result.andReturn(true);
        ret = ll.insert_results(binding, ['a']);
        expect(ret).toEqual([]);
        expect(binding.list).toEqual([]);
      });

    });

    describe("#remove_instances", function() {

      it("removes no instance when nothing is supplied to remove", function() {
        var binding = { list : [{ instance : { id : 3 }, mappings : [] }] };
        ll.remove_instance(binding, {}, 'b');
        expect(binding.list).toEqual([{ instance : { id : 3 }, mappings : [] }]);
      });

    });
/*


    , remove_instance: function(binding, instance, mappings) {
        var self = this
          , mappings
          , mapping_index
          , instance_index_to_remove = -1
          , indexes_to_remove = []
          ;

        if (!(can.isArray(mappings) || mappings instanceof can.Observe.List))
          mappings = [mappings];

        can.each(binding.list, function(data, instance_index) {
          var mapping_attr = binding.list[instance_index].mappings;

          if (data.instance.id == instance.id
              && data.instance.constructor.shortName == instance.constructor.shortName) {
            if (mapping_attr.length == 0) {
              indexes_to_remove.push(instance_index);
            } else {
              can.each(mappings, function(mapping) {
                var was_removed = data.remove_mapping(mapping);
                if (was_removed) {
                  if (mapping_attr.length == 0)
                    indexes_to_remove.push(instance_index);
                }
              });
            }
          }
        });
        can.each(indexes_to_remove.sort(), function(index_to_remove, count) {
          binding.list.splice(index_to_remove - count, 1);
        });
      }
  */
    describe("#refresh_stubs", function() {

      it("returns promise based on existing deferred, returning binding list, if it exists", function() {
        var binding = { list : [] },
            source_dfd = binding._refresh_stubs_deferred = new $.Deferred(),
            ret = ll.refresh_stubs(binding),
            sanity = false;
        source_dfd.resolve();
        ret.done(function(data) {
          expect(data).toBe(binding.list);
          sanity = true;
        });
        if(!sanity) {
          fail("sanity check failed for done callback from returned promise");
        }
      });

      it("makes new refresh stubs deferred, returning binding list, if it does not already exist", function() {
        var ret,
            binding = { list : [] },
            sanity = false;
        ll._refresh_stubs = jasmine.createSpy().andReturn($.when());
        ret = ll.refresh_stubs(binding);
        ret.done(function(data) {
          expect(data).toBe(binding.list);
          sanity = true;
        });
        if(!sanity) {
          fail("sanity check failed for done callback from returned promise");
        }
        expect(ll._refresh_stubs).toHaveBeenCalled();
      });
    });

    describe("#refresh_instances", function() {

      it("returns promise based on existing deferred, returning binding list, if it exists", function() {
        var binding = { list : [] },
            source_dfd = binding._refresh_instances_deferred = new $.Deferred(),
            ret = ll.refresh_instances(binding),
            sanity = false;
        source_dfd.resolve();
        ret.done(function(data) {
          expect(data).toBe(binding.list);
          sanity = true;
        });
        if(!sanity) {
          fail("sanity check failed for done callback from returned promise");
        }
      });

      it("makes new refresh instances deferred, returning binding list, if it does not already exist", function() {
        var ret,
            binding = { list : [] },
            sanity = false;
        ll._refresh_instances = jasmine.createSpy().andReturn($.when());
        ret = ll.refresh_instances(binding);
        ret.done(function(data) {
          expect(data).toBe(binding.list);
          sanity = true;
        });
        if(!sanity) {
          fail("sanity check failed for done callback from returned promise");
        }
        expect(ll._refresh_instances).toHaveBeenCalled();
      });
    });

    describe("#_refresh_instances", function() {

      it("returns promise based on binding list", function() {
        var ret,
            binding = { list : [{instance : 'a'}] },
            sanity = false;
        spyOn(ll, "refresh_stubs").andReturn($.when());
        spyOn(RefreshQueue.prototype, "trigger").andCallFake(function() {
          return $.when(this.objects);
        });

        ret = ll._refresh_instances(binding);
        ret.done(function(data) {
          expect(data).toEqual(['a']);
          sanity = true;
        });
        if(!sanity) {
          fail("sanity check failed for done callback from returned promise");
        }
      });

    });

  });

  describe("GGRC.ListLoaders.ReifyingListLoader", function() {

    describe("#init", function() {
      beforeEach(function() {
        spyOn(LL.BaseListLoader.prototype, "init");
      });

      it("sets source_binding property if binding is a ListBinding", function() {
        var binding = new LL.ListBinding(),
            rll = new LL.ReifyingListLoader(binding);
        expect(rll.source_binding).toBe(binding);
        expect(rll.binding).not.toBeDefined();
      });

      it("sets source property if binding is not a ListBinding", function() {
        var binding = {},
            rll = new LL.ReifyingListLoader(binding);
        expect(rll.source).toBe(binding);
        expect(rll.source_binding).not.toBeDefined();
      });

    });

    describe("#insert_from_source_binding", function() {
      beforeEach(function() {
        spyOn(RefreshQueue.prototype, "trigger").andCallFake(function() {
          return $.when(this.objects);
        });
      });

      it("makes a new binding referencing the instance and old mappings", function() {
        var rll = new LL.ReifyingListLoader(),
            binding = {},
            results = [rll.make_result('a', [])],
            expected = [rll.make_result(results[0].instance, results, {})];
        spyOn(rll, "insert_results");
        rll.insert_from_source_binding(binding, results);
        expect(rll.insert_results).toHaveBeenCalledWith(binding, expected);
      });
    });

    describe("#init_listeners", function() {

      var rll, binding, source_binding;
      beforeEach(function() {
        source_binding = new LL.ListBinding();
        binding = new LL.ListBinding();
      });
      it("sets up source_binding on the binding from the ReifyingListLoader's source_binding, if it exists", function() {
        rll = new LL.ReifyingListLoader(source_binding);
        spyOn(rll, "insert_from_source_binding");
        rll.init_listeners(binding);
        expect(binding.source_binding).toBe(source_binding);
        console.log(source_binding.list)
        expect(rll.insert_from_source_binding).toHaveBeenCalledWith(binding, source_binding.list, 0);
      });

      it("sets up source_binding from the binding via get_binding, if the source_binding property does not exist", function() {
        rll = new LL.ReifyingListLoader("dummy_binding");
        spyOn(rll, "insert_from_source_binding");
        binding = { instance : { "get_binding" : function() { return source_binding; }}};
        rll.init_listeners(binding);
        expect(binding.source_binding).toBe(source_binding);
        expect(rll.insert_from_source_binding).toHaveBeenCalledWith(binding, source_binding.list, 0);
      });

    });

    describe("listeners", function() {
      var rll, binding, source_binding;
      beforeEach(function() {
        source_binding = new LL.ListBinding();
        binding = new LL.ListBinding();
        rll = new LL.ReifyingListLoader(source_binding);
      });

      describe("source_binding.list add", function() {
        it("calls insert_from_source_binding on the list loader", function() {
          var new_result = new LL.MappingResult({id : 1}, []);
          spyOn(rll, "insert_from_source_binding");
          rll.init_listeners(binding);
          source_binding.list.push(new_result);
          expect(rll.insert_from_source_binding).toHaveBeenCalledWith(binding, [new_result], 0);
        });
      });

      describe("source_binding.list remove", function() {
        it("calls remove_instance on the list loader for each item", function() {
          var new_result = new LL.MappingResult({id : 1}, []);
          spyOn(RefreshQueue.prototype, "trigger").andReturn($.when()); //Avoid AJAX
          spyOn(rll, "remove_instance");
          binding.list.push(new_result);
          source_binding.list.push(new_result);
          rll.init_listeners(binding);
          source_binding.list.shift();
          expect(rll.remove_instance).toHaveBeenCalledWith(binding, new_result.instance, new_result);
        });
      });
    });
  });

  describe("GGRC.ListLoaders.CustomFilteredListLoader", function() {

    var cfll, binding;
    beforeEach(function() {
      binding = new LL.ListBinding();
      binding.source_binding = new LL.ListBinding();
      cfll = new LL.CustomFilteredListLoader(binding, jasmine.createSpy());
    });

    describe("_refresh_stubs", function() {

      it("gets results from binding's source binding", function() {
        var mock_inst = new GGRC.Jasmine.MockModel({ value : 'a' });
        spyOn(binding.source_binding, "refresh_instances").andReturn(new $.Deferred().reject());

        cfll._refresh_stubs(binding);
        expect(binding.source_binding.refresh_instances).toHaveBeenCalled();
      });

      it("runs all results from source binding through filter function", function() {
        var mock_inst = new GGRC.Jasmine.MockModel({ value : 'a' });
        var mock_result = { instance : mock_inst, mappings: [] };
        spyOn(binding.source_binding, "refresh_instances").andReturn(new $.Deferred().resolve([mock_result]));

        cfll._refresh_stubs(binding);
        expect(cfll.filter_fn).toHaveBeenCalledWith(mock_result);
      });

    });

    describe("listeners", function() {
      var cfll, binding, source_binding, new_result;
      beforeEach(function() {
        new_result = new LL.MappingResult({id : 1}, []);
        source_binding = new LL.ListBinding();
        binding = new LL.ListBinding();
        cfll = new LL.CustomFilteredListLoader(source_binding, jasmine.createSpy("filter_fn"));
        binding._refresh_instances_deferred = $.when();
      });

      describe("source_binding.list add", function() {
        it("calls custom filter func on the list loader", function() {
          cfll.init_listeners(binding);
          source_binding.list.push(new_result);
          expect(cfll.filter_fn).toHaveBeenCalledWith(new_result);
        });

        it("does not call the filter func when the binding has not yet been refreshed.", function() {
          delete binding._refresh_instances_deferred;
          cfll.init_listeners(binding);
          source_binding.list.push(new_result);
          expect(cfll.filter_fn).not.toHaveBeenCalled();
        });

        it("adds the new item when the filter func returns true", function() {
          var filter_result = new LL.MappingResult({id : 2}, [new_result]);
          cfll.filter_fn.andReturn(true);
          cfll.init_listeners(binding);
          spyOn(cfll, "make_result").andReturn(filter_result);
          spyOn(cfll, "insert_results");
          source_binding.list.push(new_result);
          expect(cfll.insert_results).toHaveBeenCalledWith(binding, [filter_result]);
        });

        it("does not add the new item when the filter func returns false", function() {
          var filter_result = new LL.MappingResult({id : 2}, [new_result]);
          cfll.filter_fn.andReturn(false);
          cfll.init_listeners(binding);
          spyOn(cfll, "make_result").andReturn(filter_result);
          spyOn(cfll, "insert_results");
          source_binding.list.push(new_result);
          expect(cfll.insert_results).not.toHaveBeenCalledWith(binding, [filter_result]);
          expect(cfll.insert_results).toHaveBeenCalledWith(binding, []);
        });

        it("adds the new item when the filter func returns a deferred resolving to true", function() {
          var filter_result = new LL.MappingResult({id : 2}, [new_result]);
          cfll.filter_fn.andReturn($.when(true));
          cfll.init_listeners(binding);
          spyOn(cfll, "make_result").andReturn(filter_result);
          spyOn(cfll, "insert_results");
          source_binding.list.push(new_result);
          expect(cfll.insert_results).toHaveBeenCalledWith(binding, [filter_result]);
        });

        it("does not add the new item when the filter func returns a deferred resolving to false", function() {
          var filter_result = new LL.MappingResult({id : 2}, [new_result]);
          cfll.filter_fn.andReturn($.when(false));
          cfll.init_listeners(binding);
          spyOn(cfll, "make_result").andReturn(filter_result);
          spyOn(cfll, "insert_results");
          source_binding.list.push(new_result);
          expect(cfll.insert_results).not.toHaveBeenCalledWith(binding, [filter_result]);
          expect(cfll.insert_results).toHaveBeenCalledWith(binding, []);
        });

        it("does not add the new item when the filter func returns a deferred that rejects", function() {
          var filter_result = new LL.MappingResult({id : 2}, [new_result]);
          cfll.filter_fn.andReturn(new $.Deferred().reject());
          cfll.init_listeners(binding);
          spyOn(cfll, "make_result").andReturn(filter_result);
          spyOn(cfll, "insert_results");
          source_binding.list.push(new_result);
          expect(cfll.insert_results).not.toHaveBeenCalledWith(binding, [filter_result]);
          expect(cfll.insert_results).toHaveBeenCalledWith(binding, []);
        });

      });

      describe("source_binding.list remove", function() {
        it("calls remove_instance on the list loader for each item", function() {
          var new_result = new LL.MappingResult({id : 1}, []);
          spyOn(RefreshQueue.prototype, "trigger").andReturn($.when()); //Avoid AJAX
          spyOn(cfll, "remove_instance");
          binding.list.push(new_result);
          source_binding.list.push(new_result);
          cfll.init_listeners(binding);
          source_binding.list.shift();
          expect(cfll.remove_instance).toHaveBeenCalledWith(binding, new_result.instance, new_result);
        });
      });
    });

  });

});
