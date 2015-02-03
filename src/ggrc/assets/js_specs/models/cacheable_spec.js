/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

describe("can.Model.Cacheable", function() {
  
  beforeAll(function() {
    can.Model.Mixin("dummyable");
    spyOn(CMS.Models.Mixins.dummyable, "add_to");

    can.Model.Cacheable.extend("CMS.Models.DummyModel", {
      root_object: "dummy_model",
      root_collection: "dummy_models",
      mixins: ["dummyable"],
      attributes: { dummy_attribute: "dummy_convert" },
      is_custom_attributable: true
    }, {});
  });

  afterAll(function() {
    delete CMS.Models.DummyModel;
    delete CMS.Models.Mixins.dummyable;
  });

  describe("::setup", function() {

    it("prefers pre-set static names over root object & collection", function() {
      var Model = can.Model.Cacheable.extend({
        root_object: "wrong_name",
        root_collection: "wrong_names",
        model_singular: "RightName",
        table_singular: "right_name",
        title_singular: "Right Name",
        model_plural: "RightNames",
        table_plural: "right_names",
        title_plural: "Right Names"
      }, {});
      // note that these are not explicit in beforeAll above.
      // model singular is CamelCased form of root_object
      expect(Model.model_singular).toBe("RightName");
      // table singular is under_scored version of same
      expect(Model.table_singular).toBe("right_name");
      // title singular is "Human Readable" version of same
      expect(Model.title_singular).toBe("Right Name");
      // plurals are based on root collection.
      expect(Model.model_plural).toBe("RightNames");
      expect(Model.table_plural).toBe("right_names");
      expect(Model.title_plural).toBe("Right Names");
    });

    it("sets various forms of the name based on root object & collection by default", function() {
      // note that these are not explicit in beforeAll above.
      // model singular is CamelCased form of root_object
      expect(CMS.Models.DummyModel.model_singular).toBe("DummyModel");
      // table singular is under_scored version of same
      expect(CMS.Models.DummyModel.table_singular).toBe("dummy_model");
      // title singular is "Human Readable" version of same
      expect(CMS.Models.DummyModel.title_singular).toBe("Dummy Model");
      // plurals are based on root collection.
      expect(CMS.Models.DummyModel.model_plural).toBe("DummyModels");
      expect(CMS.Models.DummyModel.table_plural).toBe("dummy_models");
      expect(CMS.Models.DummyModel.title_plural).toBe("Dummy Models");
    });

    it("sets findAll to default based on root_collection if not set", function() {
      spyOn(can.Model, "setup");
      var Model = can.Model.Cacheable.extend({ root_collection: "foos" }, {});
      expect(Model.findAll).toBe("GET /api/foos");
    });

    it("applies mixins based on the mixins property", function() {
      expect(CMS.Models.Mixins.dummyable.add_to).toHaveBeenCalledWith(CMS.Models.DummyModel);
    });

    it("merges in default attributes for created_at and updated_at", function() {
      expect(CMS.Models.DummyModel.attributes).toEqual({
        created_at: "datetime",
        updated_at: "datetime",
        dummy_attribute: "dummy_convert"
      });
    });

  });

  describe("::init", function() {

    it("sets custom attributes", function() {
      // NB using $.extend here creates a new object with all of the static properties of the function.
      //  This is how the custom attributable is implemented in setup.
      expect(GGRC.custom_attributable_types).toContain($.extend({}, CMS.Models.DummyModel));
    });

  });


  describe("::makeDestroy", function() {

    var destroy_spy;
    beforeEach(function() {
      destroy_spy = jasmine.createSpy("destroy");
      spyOn(CMS.Models.BackgroundTask, "findOne").and.returnValue($.when());
    });

    it("finds background task if specified in return object", function(done) {
      var destroy = CMS.Models.DummyModel.makeDestroy(destroy_spy);
      destroy_spy.and.returnValue($.when({ background_task: {id: 1}}));

      destroy(2).then(function() {
        expect(CMS.Models.BackgroundTask.findOne).toHaveBeenCalledWith({ id: 1 });
        done();
      }, function() {
        can.each(arguments, function(arg) {
          fail(JSON.stringify(arg));
        });
        done();
      });
    });

    it("polls background task if found", function(done) {
      var destroy = CMS.Models.DummyModel.makeDestroy(destroy_spy);
      var poll_spy = jasmine.createSpyObj("poll_spy", ["poll"]);
      destroy_spy.and.returnValue($.when({ background_task: {id: 1}}));
      CMS.Models.BackgroundTask.findOne.and.returnValue($.when(poll_spy));

      destroy(2).then(function() {
        expect(CMS.Models.BackgroundTask.findOne).toHaveBeenCalledWith({ id: 1 });
        expect(poll_spy.poll).toHaveBeenCalled();
        done();
      }, function() {
        can.each(arguments, function(arg) {
          fail(JSON.stringify(arg));
        });
        done();
      });
    });

    it("continues normally if no background task specified", function(done) {
      var destroy = CMS.Models.DummyModel.makeDestroy(destroy_spy);
      destroy_spy.and.returnValue($.when({ dummy: {id: 1}}));

      destroy(2).then(function() {
        expect(CMS.Models.BackgroundTask.findOne).not.toHaveBeenCalled();
        done();
      }, function() {
        can.each(arguments, function(arg) {
          fail(JSON.stringify(arg));
        });
        done();
      });
    });

  });

  describe("::findAll", function() {

    it("throws errors when called directly on Cacheable instead of a subclass", function() {
      expect(can.Model.Cacheable.findAll).toThrow(
        "No default findAll() exists for subclasses of Cacheable"
      );
    });
  });

  describe("::findPage", function() {
    it("throws errors when called directly on Cacheable instead of a subclass", function() {
      expect(can.Model.Cacheable.findPage).toThrow(
       "No default findPage() exists for subclasses of Cacheable"
      );
    });
  
  });

  describe("#refresh", function() {

    var inst;
    beforeEach(function() {
      inst = new CMS.Models.DummyModel({ href : '/api/dummy_models/1' });
      spyOn($, "ajax").and.returnValue(new $.Deferred(function(dfd) {
        setTimeout(function() {
          dfd.resolve(inst.serialize());
        }, 10);
      }));
    });
    afterEach(function() {
      delete CMS.Models.DummyModel.cache[undefined];
    });

    it("calls the object endpoint with the supplied href if no selfLink", function(done) {
      inst.refresh().then(function() {
        expect($.ajax).toHaveBeenCalledWith(jasmine.objectContaining({
          url: "/api/dummy_models/1",
          type: "get"
        }));
        done();
      }, fail);
    });

    it("throttles the requests to once per second", function(done) {
      inst.refresh();
      inst.refresh();
      setTimeout(function() {
        inst.refresh().then(function() {
          expect($.ajax.calls.count()).toBe(2);
          done();
        }, fail);
      }, 1000); // 1000ms is enough to trigger a new call to the debounced function
      inst.refresh().then(function() {
        expect($.ajax.calls.count()).toBe(1);
      }, fail);
    });

    it("backs up the refreshed state immediately after refreshing", function(done) {
      spyOn(CMS.Models.DummyModel, "model").and.returnValue(inst);
      spyOn(inst, "backup");
      inst.refresh().then(function() {
        expect(inst.backup).toHaveBeenCalled();
        done();
      }, fail);
    });
  });


});
