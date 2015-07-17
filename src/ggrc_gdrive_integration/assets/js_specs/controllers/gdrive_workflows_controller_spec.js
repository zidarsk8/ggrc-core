/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

window.GGRC = window.GGRC || {};
GGRC.config = GGRC.config || {};
GGRC.config.GAPI_ADMIN_GROUP = GGRC.config.GAPI_ADMIN_GROUP || "admins@example.com";

describe("GDrive Workflows Controller", function() {
  var ctl;
  beforeAll(function(done) {
    waitsFor(function() {
      return (ctl = $(document.body).control(GGRC.Controllers.GDriveWorkflow));
    }, done);
  });
  describe("#update_permission_for", function() {

    var item, permissionId, role, saved_object;
    beforeEach(function() {
      item = new CMS.Models.GDriveFolder({
        id : "a folder id"
        , userPermission : {
          role : "writer"
        }
      });
      permissionId = "permission id";
      role = "writer";
      saved_object = undefined;

      spyOn(CMS.Models.GDriveFolderPermission.prototype, "save").and.callFake(function() {
        saved_object = this;
        expect(saved_object.folder).toBe(item);
        expect(saved_object.role).toBe(role);
        return $.when();
      });
    });

    it("creates permission object for user by email address", function() {
      var person = "foo@example.com";

      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions").and.callFake(function() { return $.when([]); });

      ctl.update_permission_for(item, person, permissionId, role);
      expect(saved_object).toBeDefined();
      expect(saved_object.email).toBe(person);
      expect(saved_object.permission_type).toBe("user");
    });

    it("creates permission object for user by Person object", function() {
      var person = new CMS.Models.Person({
        id : 1
        , email : "foo@example.com"
      });

      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions").and.callFake(function() { return $.when([]); });

      ctl.update_permission_for(item, person, permissionId, role);
      expect(saved_object).toBeDefined();
      expect(saved_object.email).toBe(person.email);
      expect(saved_object.permission_type).toBe("user");
    });

    it("creates group permission object when passed Admin group", function() {
      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions").and.callFake(function() { return $.when([]); });

      ctl.update_permission_for(item, GGRC.config.GAPI_ADMIN_GROUP, permissionId, role);
      expect(saved_object).toBeDefined();
      expect(saved_object.email).toBe(GGRC.config.GAPI_ADMIN_GROUP);
      expect(saved_object.permission_type).toBe("group");
    });

    it("creates writer permission for users who currently have reader", function() {
      var person = "foo@example.com";

      spyOn(CMS.Models.GDriveFolder.prototype, "findPermissions")
      .and.callFake(function() {
        return $.when([{
          "id" : permissionId
          , "email" : person
          , "role" : "reader"
        }]);
      });

      ctl.update_permission_for(item, person, permissionId, role);
      expect(saved_object).toBeDefined();
      expect(saved_object.email).toBe(person);
      expect(saved_object.permission_type).toBe("user");
    });

    afterEach(function() {
      delete CMS.Models.GDriveFolder.cache;
      delete CMS.Models.GDriveFolderPermission.cache;
    });
  });

  describe("#create_folder_if_nonexistent", function() {

    describe("given a Program", function() {

      it("calls out to create_program_folder and does nothing else", function() {
        var program = new CMS.Models.Program({
          id : 1
          , title : "a program"
        });
        var original_create_folder = ctl.create_folder_if_nonexistent;
        spyOn(program, "get_mapping").and.returnValue([]);

        spyOn(ctl, "create_folder_if_nonexistent").and.throwError("ERROR: function tried calling itself for parent object");
        spyOn(ctl.request_create_queue, "push").and.throwError("ERROR: function pushed Program folder creation onto the Request queue");
        spyOn(ctl, "link_request_to_new_folder_or_audit_folder").and.throwError("ERROR: function tried linking a Program to an Audit's folder");

        spyOn(ctl, "create_program_folder");
        //get a little tricky.  We're already spying on the SUT, so go through it
        original_create_folder.call(ctl, program);
        expect(ctl.create_program_folder).toHaveBeenCalledWith(program.constructor, jasmine.any(Object), program);
      });

    });

    describe("given an Audit", function() {
      var audit;
      beforeEach(function() {
        audit = new CMS.Models.Audit({
          id : 1
          , title : "an audit"
          , program : new CMS.Models.Program({ id : 1 })
          , requests : []
        });
        spyOn(can.Model.Cacheable.prototype, "get_mapping").and.returnValue([]);
        spyOn(ctl, "create_audit_folder").and.returnValue($.when());
        spyOn(ctl, "create_program_folder").and.returnValue($.when());
      });

      it("recursively calls for program", function() {
        var original_create_folder = ctl.create_folder_if_nonexistent;
        spyOn(ctl, "create_folder_if_nonexistent").and.returnValue($.when());
        original_create_folder.call(ctl, audit);
        expect(ctl.create_folder_if_nonexistent).toHaveBeenCalledWith(jasmine.any(CMS.Models.Program));
      });

      it("calls out to create_audit_folder", function() {

        spyOn(ctl.request_create_queue, "push").and.throwError("ERROR: function pushed audit folder creation onto the Request queue");
        spyOn(ctl, "link_request_to_new_folder_or_audit_folder").and.throwError("ERROR: function tried linking a audit to another Audit's folder");
        //get a little tricky.  We're already spying on the SUT, so go through it
        ctl.create_folder_if_nonexistent(audit);
        expect(ctl.create_audit_folder).toHaveBeenCalledWith(audit.constructor, jasmine.any(Object), audit);
      });

      it("links in Requests that have no objectives", function() {
        var request = new CMS.Models.Request({
          id : 1
          , audit : audit
        });
        var sanity = false;
        audit.requests.push(request);
        spyOn(CMS.Models.ObjectFolder.prototype, "save").and.callFake(function() {
          sanity = true;
          expect(this instanceof CMS.Models.ObjectFolder).toBe(true);
          expect(this.folderable.reify()).toBe(request);
        });
        spyOn(RefreshQueue.prototype, "trigger").and.returnValue($.when([request]));
        ctl.create_folder_if_nonexistent(audit);
        expect(sanity).toBe(true);
      });


    });

    describe("given a Request", function() {

      var request;
      beforeEach(function() {
        request = new CMS.Models.Request({
          id : 1
          , audit : new CMS.Models.Audit({
            id : 1
            , program : new CMS.Models.Program({ id : 1 }) })
        });
        request.audit.reify().attr("requests", [request]);
        spyOn(can.Model.Cacheable.prototype, "get_mapping").and.returnValue([]);
        spyOn(can.Model.Cacheable.prototype, "get_binding").and.returnValue({ refresh_instances : function() { return $.when(); }});
        spyOn(ctl, "link_request_to_new_folder_or_audit_folder");
        spyOn(ctl.request_create_queue, "push");

        spyOn(ctl, "create_audit_folder").and.returnValue($.when());
        spyOn(ctl, "create_program_folder").and.returnValue($.when());
        spyOn(RefreshQueue.prototype, "trigger").and.returnValue($.when());
      });

      it("recursively creates an audit folder", function() {
        ctl.create_folder_if_nonexistent(request);
        expect(ctl.create_audit_folder).toHaveBeenCalledWith(request.audit.reify().constructor, jasmine.any(Object), request.audit.reify());
      });

      it("calls out to create_request_folder if audit is created", function() {
        ctl.request_create_queue.push.and.throwError("ERROR: queued request when audit create was not in progress");
        can.Model.Cacheable.prototype.get_mapping.and.callFake(function() {
          if(this instanceof CMS.Models.Audit) {
            return [{}];
          } else {
            return [];
          }
        });
        ctl.create_folder_if_nonexistent(request);
        expect(ctl.link_request_to_new_folder_or_audit_folder).toHaveBeenCalledWith(request.constructor, jasmine.any(Object), request);
      });

      it("queues Request if Audit create is in progress", function() {
        try {
          ctl._audit_create_in_progress = true;
          ctl.link_request_to_new_folder_or_audit_folder.and.throwError("ERROR: created request folder while audit create is in progress");
          ctl.create_folder_if_nonexistent(request);
          expect(ctl.request_create_queue.push).toHaveBeenCalledWith(request);
        } finally {
          delete ctl._audit_create_in_progress;
        }
      });

    });


  });

  afterEach(function() {
    delete CMS.Models.Program.cache;
    delete CMS.Models.Audit.cache;
    delete CMS.Models.Request.cache;
    delete CMS.Models.ObjectFolder.cache;
    delete CMS.Models.UserRole.cache;
    delete CMS.Models.Role.cache;
  });

});
